function main(splash)
    splash.private_mode_enabled = false
    splash.images_enabled = false
    splash.plugins_enabled = true
    splash.resource_timeout = 30.0
    local url = splash.args.url
    local button_path = splash.args.button_path
    print(button_path)

    assert(splash:go(url))
    assert(splash:wait(5))

    local button = splash:select(button_path)
    if button then
        assert(button:mouse_click())
        assert(splash:wait(5))
    else
        error("Button not found")
    end

    return {
        html = splash:html()
    }
end