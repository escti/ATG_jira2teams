#!/usr/bin/perl
use strict;
use warnings;

# Improved input validation

# Subroutine to sanitize input
sub sanitize_input {
    my ($input) = @_;
    $input =~ s/[^a-zA-Z0-9_ ]//g;  # Allow only alphanumeric and underscores
    return $input;
}

# Subroutine for input validation
sub validate_input {
    my ($input) = @_;
    if ($input =~ /^\w{1,20}$/) {  # Validate using regex
        return 1;
    }
    return 0;
}

# Main script logic
my $user_input = param('user_input');  # Assuming user input is obtained from a form

# Sanitize the input
$user_input = sanitize_input($user_input);

# Validate the sanitized input
if (validate_input($user_input)) {
    # Process the valid user input
} else {
    print "Content-type: text/html\n\n";
    print "<h2>Error: Invalid input!</h2>";
}
