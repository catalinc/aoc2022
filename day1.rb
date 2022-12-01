# frozen_string_literal: true

inventory = []

IO.foreach('input/day1.txt', '') { |paragraph| inventory << paragraph.split.map(&:to_i) }

calories_per_elf = inventory.map(&:sum)

# part 1
puts calories_per_elf.max

# part 2
calories_per_elf.sort! { |x, y| y <=> x }
puts calories_per_elf[0, 3].sum
