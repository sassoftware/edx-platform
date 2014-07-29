class Badges.Views.BadgeInstancesScrollbar extends Backbone.View

  template: _.template($("#badgeinstance_scrollbar-tpl").html())

  #events:
  #  'click #badgeinstance_table': 'table_clicked'

  initialize: -> 
    console.log("Initializing BadgeInstancesScrollBar")
    @collection.on('reset', @render, this)
    @collection.on('add', @appendEntry, this) 


  render: -> 
    $(@el).html(@template()) 
    self = this
    #@collection.toJSON().forEach (student) -> 
    #  self.appendEntry(student)
    @collection.forEach (student_badgeinstance) -> 
      self.appendEntry(student_badgeinstance.toJSON())
    this

  appendEntry: (student_badgeinstance) =>
    view = new Badges.Views.BadgeInstance(model: student_badgeinstance)
    @$('#badgeinstance_scrollbar').append(view.render().el) 

  table_clicked: (event) ->
    alert "We clicked the table"


      
  handleError: (entry, response) ->
    if response.status == 422
      errors = $.parseJSON(response.responseText).errors
      for attribute, messages of errors
        alert "#{attribute} #{message}" for message in messages