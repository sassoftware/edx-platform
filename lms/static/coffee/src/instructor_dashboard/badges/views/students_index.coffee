class Badges.Views.StudentsIndex extends Backbone.View

  template: _.template($("#student_table-tpl").html())

  #events:
  #  'click #student_badge_table': 'table_clicked'

  initialize: -> 
    @collection.on('reset', @render, this)
    @collection.on('add', @appendEntry, this) 

  render: -> 
    $(@el).html(@template()) 
    self = this
    #@collection.toJSON().forEach (student) -> 
    #  self.appendEntry(student)
    @collection.forEach (student) -> 
      self.appendEntry(student.toJSON())
    this

  appendEntry: (student) =>
    view = new Badges.Views.StudentEntry(model: student)
    @$('#student_badge_table_tbody').append(view.render().el) 

  table_clicked: (event) ->
    alert "We clicked the table"


      
  handleError: (entry, response) ->
    if response.status == 422
      errors = $.parseJSON(response.responseText).errors
      for attribute, messages of errors
        alert "#{attribute} #{message}" for message in messages