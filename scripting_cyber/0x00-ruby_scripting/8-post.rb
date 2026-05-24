require 'net/http'
require 'uri'
require 'json'

# Performs an HTTP POST request to the specified URL with body parameters
def post_request(url, body_params)
  # 1. Parse the string URL into a URI object
  uri = URI.parse(url)

  # 2. Create the Net::HTTP object and enable SSL if the URL uses HTTPS
  http = Net::HTTP.new(uri.host, uri.port)
  http.use_ssl = (uri.scheme == 'https')

  # 3. Initialize the POST request with the destination path
  request = Net::HTTP::Post.new(uri.path)
  
  # 4. Set the body parameters (URL-encoded form data)
  request.set_form_data(body_params)

  # 5. Send the request and capture the response
  response = http.request(request)

  # 6. Print the response status code and message (e.g., "201 Created")
  puts "Response status: #{response.code} #{response.message}"

  # 7. Parse and pretty print the response body
  parsed_body = JSON.parse(response.body)
  puts "Response body:"
  puts JSON.pretty_generate(parsed_body)
end
