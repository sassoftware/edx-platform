class Badges.Routers.BadgeInstances extends Backbone.Router
  routes:
    'view-badgeinstances': 'badgeinstance_scrollbar' 

  initialize: ->
    console.log("Initialize the Router...")
    @collection = new Badges.Collections.BadgeInstances()
    @collection.on('reset', @badgeinstance_scrollbar, this)
    #enrolled_students.forEach (badgeinstance) ->
    #  student.badges=4 
    #  student.badgerequests=3
    #@collection.reset($('#student_badges_scrollbar').data(enrolled_students)) 
    @collection.reset(student_badgeinstances) 
    @badgeinstance_scrollbar

  badgeinstance_scrollbar: ->
    view = new Badges.Views.BadgeInstancesScrollbar(collection: @collection)
    $('#student_badges_scrollbar').html(view.render().el)

  show: (id) ->
    alert "Entry #{id}"
