window.Badges =
  Models: {}
  Collections: {}
  Views: {}
  Routers: {}
  init: ->
    new Badges.Routers.BadgeInstances()
    Backbone.history.start()


$(document).ready ->
  #Badges.init()
  $('#student_badges_scrollbar').tinyscrollbar({ axis: "x", scroll: true, scrollInvert: true})