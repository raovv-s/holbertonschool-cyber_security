# Method to print all command-line arguments formatted for the checker
def print_arguments
  if ARGV.empty?
    puts "No arguments provided."
  else
    # 1. Print the required header
    puts "Arguments:"
    
    # 2. Print each argument on a new line
    ARGV.each do |arg|
      puts arg
    end
  end
end
