function main(splash)
    splash.private_mode_enabled = false
    splash.images_enabled = false
    splash.plugins_enabled = true
    splash.resource_timeout = 30.0
    local url = splash.args.url
    local scroll_button_path = splash.args.button_path
    local sec
    if splash.args.fast_load == "true" then
	    sec = 1
	 else
	    sec = 5
    end

    assert(splash:go(url))
    assert(splash:wait(sec))

   local button = splash:select(scroll_button_path)

    if button then
        assert(button:mouse_click())
        assert(splash:wait(sec))
    else
        error("Button not found")
    end

    return {
        html = splash:html()
    }
end