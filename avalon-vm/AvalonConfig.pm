package AvalonConfig;

use YAML::XS;
use XML::Twig;
use Data::Dumper;

our $LOG = "/root/avalon-setup.log";

sub log {
    my($filename, $message) = @_;
    open(H, ">>$LOG");
    printf H "[%s][%s] %s\n", $filename, scalar(localtime), $message;
    close(H);
}

sub randomPass {
    if(!scalar(@words)) {
	open(H, "/usr/share/dict/words");
	while(<H>) {
	    chomp;
	    if(m/^[a-zA-Z]+$/) {
		push(@words, $_);
	    }
	}
	close(H);
    }
    my @pass = ($words[int(rand(scalar(@words)))],
		$words[int(rand(scalar(@words)))],
		$words[int(rand(scalar(@words)))]);
    return sprintf("%s_%s_%s", @pass);
}






package AvalonConfig::YAML;

sub new {
    my($class, $filename) = @_;
    my $self = {
	'filename' => $filename,
	'yaml' => YAML::XS::LoadFile($filename),
    };
    return bless $self, $class;
}

sub close {
    my($self) = @_;
    YAML::XS::DumpFile($self->{filename}, $self->{yaml});
}

sub set {
    my($self, $name, $data) = @_;
    my(@parts) = split(/\./, $name);
    my $field = pop(@parts);
    my $here = $self->{yaml};
    foreach my $p (@parts) {
	if(exists($here->{$p})) {
	    $here = $here->{$p};
	} else {
	    $here->{$p} = {};
	    $here = $here->{$p};
	}
    }
    AvalonConfig::log($self->{filename}, "Setting $name to \'$data\'");
    $here->{$field} = $data;
}

sub get {
    my($self, $name) = @_;
    my(@parts) = split(/\./, $name);
    my $here = $self->{yaml};
    foreach my $p (@parts) {
	if(exists($here->{$p})) {
	    $here = $here->{$p};
	} else {
	    return undef;
	}
    }
    return $here;
}

package AvalonConfig::Properties;

sub new {
    my($class, $filename) = @_;
    my $self = {
	'filename' => $filename,
	'data' => [],
    };
    open(H, $filename);
    while(<H>) {
	push(@{$self->{data}}, $_);
    }
    close(H);
    return bless $self, $class;
}

sub close {
    my($self) = @_;
    open(H, ">$self->{filename}");
    foreach (@{$self->{data}}) {
	print H;
    }
    close(H);
}

sub set {
    my($self, $name, $data) = @_;
    my $set = 0;
    foreach (@{$self->{data}}) {
	if(m/^\s*$name\s*=\s*/) {
	    AvalonConfig::log($self->{filename}, "Setting $name to \'$data\'");
	    $_ = "$name=$data\n";
	    $set = 1;
	    last;
	}	
    }
    if(!$set) {
	push(@{$self->{data}}, "$name=$data\n");
    }
}

sub get {
    my($self, $name) = @_;
    foreach (@{$self->{data}}) {
	if(m/^\s*$name\s*=\s*(.+)/) {
	    return $1;
	}
    }
}

package AvalonConfig::Text;
sub new {
    my($class, $filename) = @_;
    my $self = {
	'filename' => $filename,
	'data' => [],
    };
    open(H, $filename);
    while(<H>) {
	push(@{$self->{data}}, $_);
    }
    close(H);
    return bless $self, $class;
}

sub close {
    my($self) = @_;
    open(H, ">$self->{filename}");
    foreach (@{$self->{data}}) {
	print H;
    }
    close(H);
}

sub set {
    my($self, $name, $data) = @_;
    my $set = 0;
    foreach (@{$self->{data}}) {
	if(m/^$name/i) {
	    AvalonConfig::log($self->{filename}, "Modifying\n  $_  to\n  $data");
	    $_ = "$data\n";
	    $set = 1;
	    last;
	}	
    }
    if(!$set) {
	push(@{$self->{data}}, "$data\n");
    }
}

sub get {
    my($self, $name) = @_;
    foreach (@{$self->{data}}) {
	if(m/^$name/i) {
	    return $_;
	}
    }
}

package AvalonConfig::XML;
sub transform {
    my($class, $filename, $handlers, $log) = @_;
    my $t = XML::Twig->new(twig_handlers => $handlers,
			   pretty_print => 'indented');
    $t->parsefile($filename);
    $t->print_to_file($filename);
    AvalonConfig::log($filename, $log);
}



1;
