"""
Tests for discussion pages
"""

from uuid import uuid4

from .helpers import UniqueCourseTest
from ..pages.studio.auto_auth import AutoAuthPage
from ..pages.lms.courseware import CoursewarePage
from ..pages.lms.discussion import (
    DiscussionTabSingleThreadPage,
    InlineDiscussionPage,
    InlineDiscussionThreadPage
)
from ..fixtures.course import CourseFixture, XBlockFixtureDesc
from ..fixtures.discussion import SingleThreadViewFixture, Thread, Response, Comment


class DiscussionResponsePaginationTestMixin(object):
    """
    A mixin containing tests for response pagination for use by both inline
    discussion and the discussion tab
    """

    def setup_thread(self, num_responses, **thread_kwargs):
        """
        Create a test thread with the given number of responses, passing all
        keyword arguments through to the Thread fixture, then invoke
        setup_thread_page.
        """
        thread_id = "test_thread_{}".format(uuid4().hex)
        thread_fixture = SingleThreadViewFixture(
            Thread(id=thread_id, commentable_id=self.discussion_id, **thread_kwargs)
        )
        for i in range(num_responses):
            thread_fixture.addResponse(Response(id=str(i), body=str(i)))
        thread_fixture.push()
        self.setup_thread_page(thread_id)

    def assert_response_display_correct(self, response_total, displayed_responses):
        """
        Assert that various aspects of the display of responses are all correct:
        * Text indicating total number of responses
        * Presence of "Add a response" button
        * Number of responses actually displayed
        * Presence and text of indicator of how many responses are shown
        * Presence and text of button to load more responses
        """
        self.assertEqual(
            self.thread_page.get_response_total_text(),
            str(response_total) + " responses"
        )
        self.assertEqual(self.thread_page.has_add_response_button(), response_total != 0)
        self.assertEqual(self.thread_page.get_num_displayed_responses(), displayed_responses)
        self.assertEqual(
            self.thread_page.get_shown_responses_text(),
            (
                None if response_total == 0 else
                "Showing all responses" if response_total == displayed_responses else
                "Showing first {} responses".format(displayed_responses)
            )
        )
        self.assertEqual(
            self.thread_page.get_load_responses_button_text(),
            (
                None if response_total == displayed_responses else
                "Load all responses" if response_total - displayed_responses < 100 else
                "Load next 100 responses"
            )
        )

    def test_pagination_no_responses(self):
        self.setup_thread(0)
        self.assert_response_display_correct(0, 0)

    def test_pagination_few_responses(self):
        self.setup_thread(5)
        self.assert_response_display_correct(5, 5)

    def test_pagination_two_response_pages(self):
        self.setup_thread(50)
        self.assert_response_display_correct(50, 25)

        self.thread_page.load_more_responses()
        self.assert_response_display_correct(50, 50)

    def test_pagination_exactly_two_response_pages(self):
        self.setup_thread(125)
        self.assert_response_display_correct(125, 25)

        self.thread_page.load_more_responses()
        self.assert_response_display_correct(125, 125)

    def test_pagination_three_response_pages(self):
        self.setup_thread(150)
        self.assert_response_display_correct(150, 25)

        self.thread_page.load_more_responses()
        self.assert_response_display_correct(150, 125)

        self.thread_page.load_more_responses()
        self.assert_response_display_correct(150, 150)

    def test_add_response_button(self):
        self.setup_thread(5)
        self.assertTrue(self.thread_page.has_add_response_button())
        self.thread_page.click_add_response_button()

    def test_add_response_button_closed_thread(self):
        self.setup_thread(5, closed=True)
        self.assertFalse(self.thread_page.has_add_response_button())


class DiscussionTabSingleThreadTest(UniqueCourseTest, DiscussionResponsePaginationTestMixin):
    """
    Tests for the discussion page displaying a single thread
    """

    def setUp(self):
        super(DiscussionTabSingleThreadTest, self).setUp()
        self.discussion_id = "test_discussion_{}".format(uuid4().hex)

        # Create a course to register for
        CourseFixture(**self.course_info).install()

        AutoAuthPage(self.browser, course_id=self.course_id).visit()

    def setup_thread_page(self, thread_id):
        self.thread_page = DiscussionTabSingleThreadPage(self.browser, self.course_id, thread_id)  # pylint:disable=W0201
        self.thread_page.visit()


class DiscussionCommentDeletionTest(UniqueCourseTest):
    """
    Tests for deleting comments displayed beneath responses in the single thread view.
    """

    def setUp(self):
        super(DiscussionCommentDeletionTest, self).setUp()

        # Create a course to register for
        CourseFixture(**self.course_info).install()

    def setup_user(self, roles=[]):
        roles_str = ','.join(roles)
        self.user_id = AutoAuthPage(self.browser, course_id=self.course_id, roles=roles_str).visit().get_user_id()

    def setup_view(self):
        view = SingleThreadViewFixture(Thread(id="comment_deletion_test_thread"))
        view.addResponse(
            Response(id="response1"),
            [Comment(id="comment_other_author", user_id="other"), Comment(id="comment_self_author", user_id=self.user_id)])
        view.push()

    def test_comment_deletion_as_student(self):
        self.setup_user()
        self.setup_view()
        page = DiscussionTabSingleThreadPage(self.browser, self.course_id, "comment_deletion_test_thread")
        page.visit()
        self.assertTrue(page.is_comment_deletable("comment_self_author"))
        self.assertTrue(page.is_comment_visible("comment_other_author"))
        self.assertFalse(page.is_comment_deletable("comment_other_author"))
        page.delete_comment("comment_self_author")

    def test_comment_deletion_as_moderator(self):
        self.setup_user(roles=['Moderator'])
        self.setup_view()
        page = DiscussionTabSingleThreadPage(self.browser, self.course_id, "comment_deletion_test_thread")
        page.visit()
        self.assertTrue(page.is_comment_deletable("comment_self_author"))
        self.assertTrue(page.is_comment_deletable("comment_other_author"))
        page.delete_comment("comment_self_author")
        page.delete_comment("comment_other_author")


class DiscussionCommentEditTest(UniqueCourseTest):
    """
    Tests for editing comments displayed beneath responses in the single thread view.
    """

    def setUp(self):
        super(DiscussionCommentEditTest, self).setUp()

        # Create a course to register for
        CourseFixture(**self.course_info).install()

    def setup_user(self, roles=[]):
        roles_str = ','.join(roles)
        self.user_id = AutoAuthPage(self.browser, course_id=self.course_id, roles=roles_str).visit().get_user_id()

    def setup_view(self):
        view = SingleThreadViewFixture(Thread(id="comment_edit_test_thread"))
        view.addResponse(
            Response(id="response1"),
            [Comment(id="comment_other_author", user_id="other"), Comment(id="comment_self_author", user_id=self.user_id)])
        view.push()

    def edit_comment(self, page, comment_id):
        page.start_comment_edit(comment_id)
        new_comment = "edited body"
        page.set_comment_editor_value(comment_id, new_comment)
        page.submit_comment_edit(comment_id, new_comment)

    def test_edit_comment_as_student(self):
        self.setup_user()
        self.setup_view()
        page = DiscussionTabSingleThreadPage(self.browser, self.course_id, "comment_edit_test_thread")
        page.visit()
        self.assertTrue(page.is_comment_editable("comment_self_author"))
        self.assertTrue(page.is_comment_visible("comment_other_author"))
        self.assertFalse(page.is_comment_editable("comment_other_author"))
        self.edit_comment(page, "comment_self_author")

    def test_edit_comment_as_moderator(self):
        self.setup_user(roles=["Moderator"])
        self.setup_view()
        page = DiscussionTabSingleThreadPage(self.browser, self.course_id, "comment_edit_test_thread")
        page.visit()
        self.assertTrue(page.is_comment_editable("comment_self_author"))
        self.assertTrue(page.is_comment_editable("comment_other_author"))
        self.edit_comment(page, "comment_self_author")
        self.edit_comment(page, "comment_other_author")

    def test_cancel_comment_edit(self):
        self.setup_user()
        self.setup_view()
        page = DiscussionTabSingleThreadPage(self.browser, self.course_id, "comment_edit_test_thread")
        page.visit()
        self.assertTrue(page.is_comment_editable("comment_self_author"))
        original_body = page.get_comment_body("comment_self_author")
        page.start_comment_edit("comment_self_author")
        page.set_comment_editor_value("comment_self_author", "edited body")
        page.cancel_comment_edit("comment_self_author", original_body)

    def test_editor_visibility(self):
        """Only one editor should be visible at a time within a single response"""
        self.setup_user(roles=["Moderator"])
        self.setup_view()
        page = DiscussionTabSingleThreadPage(self.browser, self.course_id, "comment_edit_test_thread")
        page.visit()
        self.assertTrue(page.is_comment_editable("comment_self_author"))
        self.assertTrue(page.is_comment_editable("comment_other_author"))
        self.assertTrue(page.is_add_comment_visible("response1"))
        original_body = page.get_comment_body("comment_self_author")
        page.start_comment_edit("comment_self_author")
        self.assertFalse(page.is_add_comment_visible("response1"))
        self.assertTrue(page.is_comment_editor_visible("comment_self_author"))
        page.set_comment_editor_value("comment_self_author", "edited body")
        page.start_comment_edit("comment_other_author")
        self.assertFalse(page.is_comment_editor_visible("comment_self_author"))
        self.assertTrue(page.is_comment_editor_visible("comment_other_author"))
        self.assertEqual(page.get_comment_body("comment_self_author"), original_body)
        page.start_response_edit("response1")
        self.assertFalse(page.is_comment_editor_visible("comment_other_author"))
        self.assertTrue(page.is_response_editor_visible("response1"))
        original_body = page.get_comment_body("comment_self_author")
        page.start_comment_edit("comment_self_author")
        self.assertFalse(page.is_response_editor_visible("response1"))
        self.assertTrue(page.is_comment_editor_visible("comment_self_author"))
        page.cancel_comment_edit("comment_self_author", original_body)
        self.assertFalse(page.is_comment_editor_visible("comment_self_author"))
        self.assertTrue(page.is_add_comment_visible("response1"))


class InlineDiscussionTest(UniqueCourseTest, DiscussionResponsePaginationTestMixin):
    """
    Tests for inline discussions
    """

    def setUp(self):
        super(InlineDiscussionTest, self).setUp()
        self.discussion_id = "test_discussion_{}".format(uuid4().hex)
        CourseFixture(**self.course_info).add_children(
            XBlockFixtureDesc("chapter", "Test Section").add_children(
                XBlockFixtureDesc("sequential", "Test Subsection").add_children(
                    XBlockFixtureDesc("vertical", "Test Unit").add_children(
                        XBlockFixtureDesc(
                            "discussion",
                            "Test Discussion",
                            metadata={"discussion_id": self.discussion_id}
                        )
                    )
                )
            )
        ).install()

        AutoAuthPage(self.browser, course_id=self.course_id).visit()

        CoursewarePage(self.browser, self.course_id).visit()
        self.discussion_page = InlineDiscussionPage(self.browser, self.discussion_id)

    def setup_thread_page(self, thread_id):
        self.discussion_page.expand_discussion()
        self.assertEqual(self.discussion_page.get_num_displayed_threads(), 1)
        self.thread_page = InlineDiscussionThreadPage(self.browser, thread_id)  # pylint:disable=W0201
        self.thread_page.expand()

    def test_initial_render(self):
        self.assertFalse(self.discussion_page.is_discussion_expanded())

    def test_expand_discussion_empty(self):
        self.discussion_page.expand_discussion()
        self.assertEqual(self.discussion_page.get_num_displayed_threads(), 0)
