@XBlock =
  Runtime: {}

  initializeBlock: (element) ->
    $element = $(element)
    children = @initializeBlocks($element)
    runtime = $element.data("runtime-class")
    version = $element.data("runtime-version")
    initFnName = $element.data("init")
    $element.prop('xblock_children', children)
    if runtime? and version? and initFnName?
      runtime = new window[runtime]["v#{version}"]
      initFn = window[initFnName]
      block = initFn(runtime, element) ? {}
      block.runtime = runtime
    else
      elementTag = $('<div>').append($element.clone()).html();
      console.log("Block #{elementTag} is missing data-runtime, data-runtime-version or data-init, and can't be initialized")
      block = {}

    block.element = element
    block.name = $element.data("name")

    $element.trigger("xblock-initialized")
    $element.data("initialized", true)
    $element.addClass("xblock-initialized")
    block

  initializeBlocks: (element) ->
    $(element).immediateDescendents(".xblock").map((idx, elem) =>
      @initializeBlock elem
    ).toArray()
