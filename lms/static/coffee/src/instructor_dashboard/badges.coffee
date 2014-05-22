window.Badges =
  Models: {}
  Collections: {}
  Views: {}
  Routers: {}
  init: ->
    new Badges.Routers.EnrolledStudents()
    Backbone.history.start()


$(document).ready ->
  Badges.init()