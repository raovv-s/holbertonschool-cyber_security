# Method to print all command-line arguments with their indices
def print_arguments
  # 1. Check if the ARGV array is empty
  if ARGV.empty?
    puts "No arguments provided."
  else
    # 2. Iterate through arguments with their corresponding 0-based index
    ARGV.each_with_index do |arg, index|
      # 3. Print the 1-based index and the argument value
      puts "#{index + 1}. #{arg}"
    end
  end
end
