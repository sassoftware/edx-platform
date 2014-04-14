define(["js/views/baseview", "jquery", "js/views/edit_textbook", "js/views/show_textbook"],
        function(BaseView, $, EditTextbookView, ShowTextbookView) {
    var ListTextbooks = BaseView.extend({
        initialize: function() {
            this.emptyTemplate = this.loadTemplate('no-textbooks');
            this.listenTo(this.collection, 'all', this.render);
            this.listenTo(this.collection, 'destroy', this.handleDestroy);
        },
        tagName: "div",
        className: "textbooks-list",
        render: function() {
            var textbooks = this.collection;
            if(textbooks.length === 0) {
                this.$el.html(this.emptyTemplate());
            } else {
                this.$el.empty();
                var that = this;
                textbooks.each(function(textbook) {
                    var view;
                    if (textbook.get("editing")) {
                        view = new EditTextbookView({model: textbook});
                    } else {
                        view = new ShowTextbookView({model: textbook});
                    }
                    that.$el.append(view.render().el);
                });
            }
            return this;
        },
        events: {
            "click .new-button": "addOne"
        },
        addOne: function(e) {
            if(e && e.preventDefault) { e.preventDefault(); }
            this.collection.add([{editing: true}]);
        },
        handleDestroy: function(model, collection, options) {
            collection.remove(model);
        }
    });
    return ListTextbooks;
});
