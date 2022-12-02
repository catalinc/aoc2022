# frozen_string_literal: true

INPUT_MAPPING = { 'A' => 'R', 'B' => 'P', 'C' => 'S',
                  'X' => 'R', 'Y' => 'P', 'Z' => 'S' }.freeze
SHAPE_SCORE = { 'R' => 1, 'P' => 2, 'S' => 3 }.freeze
WIN = { 'R' => 'S', 'P' => 'R', 'S' => 'P' }.freeze
LOSE =  WIN.map { |k, v| [v, k] }.to_h

def play_round(opponent, you)
  o = INPUT_MAPPING[opponent] || opponent
  y = INPUT_MAPPING[you] || you
  score = if WIN[o] == y
            0
          elsif o == y
            3
          else
            6
          end
  SHAPE_SCORE[y] + score
end

def play_round_with_outcome(opponent, outcome)
  o = INPUT_MAPPING[opponent]
  y = case outcome
      when 'X'
        WIN[o]
      when 'Y'
        o
      else
        LOSE[o]
      end
  play_round(o, y)
end

input_file = 'input/day2.txt'
input_file = ARGV[0] if ARGV.length == 1

# part 1 & 2
total_score = 0
total_score_with_strategy = 0
IO.foreach(input_file) do |line|
  opponent, you = line.strip.split(' ')
  total_score += play_round(opponent, you)
  total_score_with_strategy += play_round_with_outcome(opponent, you)
end
puts total_score
puts total_score_with_strategy
