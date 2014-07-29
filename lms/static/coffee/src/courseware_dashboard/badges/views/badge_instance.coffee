class Badges.Views.BadgeInstance extends Backbone.View

  template: _.template($("#badgeinstance_badgelet-tpl").html())

  events:
    'click': 'element_clicked'

  initialize: -> 
    #@collection.on('reset', @render, this)
    #@collection.on('add', @appendEntry, this) 

  #render: -> 
  #  @template(student: @model)
    #this
  render: -> 
    html = @template(student_badgeinstance: @model)
    @setElement($(html))
    this

  element_clicked: (event) ->
    event.preventDefault()
    alert "We clicked the Cell "+event.target.childNodes[0].textContent

      
  handleError: (entry, response) ->
    if response.status == 422
      errors = $.parseJSON(response.responseText).errors
      for attribute, messages of errors
        alert "#{attribute} #{message}" for message in messages