#!/usr/bin/env ruby
require 'fox16'
require 'open-uri'

include Fox

class URLParserApp < FXMainWindow
  def initialize(app)
    super(app, "Web Page Parser", width: 500, height: 400)

    vbox = FXVerticalFrame.new(self, LAYOUT_FILL_X | LAYOUT_FILL_Y)

    FXLabel.new(vbox, "Enter URL:")
    @url_input = FXTextField.new(vbox, 50)

    button = FXButton.new(vbox, "Fetch Page Source")
    @output = FXText.new(vbox, opts: LAYOUT_FILL_X | LAYOUT_FILL_Y)

    button.connect(SEL_COMMAND) do
      url = @url_input.text.strip
      if url.empty?
        @output.text = "Please enter a valid URL"
      else
        begin
          source = URI.open(url).read
          urls = source.scan(/https?:\/\/[^\s"'>]+/)
          unique_urls = urls.uniq.join("\n")
          @output.text = unique_urls.empty? ? "No URLs found." : unique_urls
        rescue => e
          @output.text = "Error fetching URL: #{e.message}"
        end
      end
    end
  end

  def create
    super
    show(PLACEMENT_SCREEN)
  end
end

app = FXApp.new
URLParserApp.new(app)
app.create
app.run

