class Badges.Routers.EnrolledStudents extends Backbone.Router
  routes:
    'view-badges': 'student_index' 

  initialize: ->
    @collection = new Badges.Collections.Students()
    enrolled_students.forEach (student) ->
      student.badges=4 
      student.badgerequests=3
    #@collection.reset($('#enrolled_student_table').data(enrolled_students)) 
    @collection.reset(enrolled_students) 

  student_index: ->
    view = new Badges.Views.StudentsIndex(collection: @collection)
    $('#enrolled_student_table').html(view.render().el)

  show: (id) ->
    alert "Entry #{id}"
