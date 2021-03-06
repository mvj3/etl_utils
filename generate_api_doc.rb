# encoding: UTF-8

class ValidMethod
    DefRegexp = /  def /
    IgnoreRegexp = /ignore$/
    attr_reader :api, :prefix_blank_length

    def initialize line1
        @line    = line1
        splits   = line1.split(DefRegexp)
        @api     = splits[1]
                            .gsub(/\(cls, |\(self, /, '(')
                            .gsub(/\): */, ')')
        @prefix_blank_length = splits[0].length + 2
    end

    def self.select_valid_api filename
        method_list = `cat etl_utils/#{filename}.py`.split("\n").grep(ValidMethod::DefRegexp)
                                                   .reject {|line1| IgnoreRegexp.match(line1) }
                                                   .map {|line1| ValidMethod.new(line1) }

        valid_prefix_blanks_length = method_list.map do |api|
            api.prefix_blank_length
        end.inject({}) do |dict, prefix_blank_length|
            dict[prefix_blank_length] ||= 0
            dict[prefix_blank_length] += 1
            dict
        end.sort_by {|a, b| a[1] <=> b[1] }[0][0]

        return method_list.select do |api|
            api.prefix_blank_length == valid_prefix_blanks_length
        end.map(&:api)
    end
end



def generate_api_doc
    `cat etl_utils/__init__.py`.split("\n").grep(/Utils/).each do |line1|
        match = line1.match(/from \.([a-z_]+) +import ([A-Z][a-z]+Utils)/)
        classname = match[2]
        filename  = match[1]

        ValidMethod.select_valid_api(filename).each do |api|
            puts "#{classname}.#{api}"
        end
    end
end

generate_api_doc

# Example data is
# ListUtils.most_common_inspect(list1)
