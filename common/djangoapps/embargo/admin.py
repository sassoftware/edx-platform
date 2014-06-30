"""
Django admin page for embargo models
"""
from django.contrib import admin
import textwrap

from config_models.admin import ConfigurationModelAdmin
from embargo.models import EmbargoedCourse, EmbargoedState, IPFilter
from embargo.forms import EmbargoedCourseForm, EmbargoedStateForm, IPFilterForm


class EmbargoedCourseAdmin(admin.ModelAdmin):
    """Admin for embargoed course ids"""
    form = EmbargoedCourseForm
    fieldsets = (
        (None, {
            'fields': ('course_id', 'embargoed'),
            'description': textwrap.dedent("""\
                Enter a course id in the following box.
                Do not enter leading or trailing slashes. There is no need to surround the
                course ID with quotes.
                Validation will be performed on the course name, and if it is invalid, an
                error message will display.

                To enable embargos against this course (restrict course access from embargoed
                states), check the "Embargoed" box, then click "Save".
            """)
        }),
    )


class EmbargoedStateAdmin(ConfigurationModelAdmin):
    """Admin for embargoed countries"""
    form = EmbargoedStateForm
    fieldsets = (
        (None, {
            'fields': ('enabled', 'embargoed_countries',),
            'description': textwrap.dedent("""Enter the two-letter ISO-3166-1 Alpha-2
            code of the country or countries to embargo in the following box. For help,
            see <a href="http://en.wikipedia.org/wiki/ISO_3166-1#Officially_assigned_code_elements">
            this list of ISO-3166-1 country codes</a>.

            Enter the embargoed country codes separated by a comma. Do not surround with quotes.
            """)
        }),
    )


class IPFilterAdmin(ConfigurationModelAdmin):
    """Admin for blacklisting/whitelisting specific IP addresses"""
    form = IPFilterForm
    fieldsets = (
        (None, {
            'fields': ('enabled', 'whitelist', 'blacklist'),
            'description': textwrap.dedent("""Enter specific IP addresses to explicitly
            whitelist (not block) or blacklist (block) in the appropriate box below.
            Separate IP addresses with a comma. Do not surround with quotes.
            """)
        }),
    )

admin.site.register(EmbargoedCourse, EmbargoedCourseAdmin)
admin.site.register(EmbargoedState, EmbargoedStateAdmin)
admin.site.register(IPFilter, IPFilterAdmin)
