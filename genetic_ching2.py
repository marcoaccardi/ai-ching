from music21 import note, stream, metadata
import random
import itertools
from datetime import datetime
import os


class GeneticMusic:
    def __init__(self):
        # Creates all possible combinations of 6-character strings made of 'Y' and 'N
        self.hexagrams = [''.join(h)
                          for h in itertools.product('YN', repeat=6)]
        self.modes = {
            # Ionian Mode (Major Scale) #60 71
            1: [60, 62, 64, 65, 67, 69, 71],
            2: [60, 62, 63, 65, 67, 69, 70],  # Dorian Mode # 60, 69
            3: [60, 61, 63, 65, 67, 68, 70],  # Phrygian Mode # 60, 61
            4: [60, 62, 64, 66, 67, 69, 71],  # Lydian Mode # 60, 66
            5: [60, 62, 64, 65, 67, 69, 70],  # Mixolydian Mode #60, 70
            # Aeolian Mode (Natural Minor Scale)
            6: [60, 62, 63, 65, 67, 68, 70],  # 60, 68

        }
        # Extended range for each mode
        self.extended_modes = {}
        for mode_key, mode_notes in self.modes.items():
            extended_notes = []
            # Add notes from two octaves down
            extended_notes += [note - 24 for note in mode_notes]
            # Add notes from the original octave
            extended_notes += mode_notes
            # # Add notes from one octave up
            # extended_notes += [note - 12 for note in mode_notes]
            self.extended_modes[mode_key] = extended_notes

        # Define preferred notes for each mode
        self.preferred_notes = {
            1: [60, 71],  # Ionian
            2: [60, 69],  # Dorian
            3: [60, 61],  # Phrygian
            4: [60, 66],  # Lydian
            5: [60, 70],  # Mixolydian
            6: [60, 68],  # Aeolian

        }

    # Generates an initial population of motifs (hexagrams)
    # based on a specified musical mode.
    # Each motif is a 6-character string ('Y' or 'N'),
    # representing the presence or absence of a note.
    def generate_initial_population(self, size=10, mode=None):
        # eventually contain all the generated motifs
        population = []
        preferred_notes = self.preferred_notes[mode] if mode in self.preferred_notes else [
        ]

        for _ in range(size):
            motif = ''
            # each motif is built as a string of 'Y' and 'N' characters,
            # where 'Y' represents the presence of a note and 'N' represents its absence.
            for i in range(6):  # Assuming a motif length of 6
                # selects a note from the current mode's scale.
                # The % operator ensures that the index i wraps around
                # if it exceeds the length of the mode's scale,
                # allowing for cyclic selection of notes.
                note = self.modes[mode][i % len(self.modes[mode])]
                # Increase probability for preferred notes
                if note in preferred_notes:
                    # appends 'Y' to motif with a probability of 0.6 (60%),
                    motif += 'Y' if random.random() < 0.6 else 'N'
                else:
                    # it randomly appends either 'Y' or 'N' with equal probability.
                    motif += random.choice(['Y', 'N'])
            population.append(motif)

        return population
    # Evaluates a motif's fitness based on multiple musical factors,
    # including conformity to scale, melodic interest,
    # rhythmic complexity, motivic development potential,
    # and repetition/variation.

    def fitness_function(self, motif, mode):
        score = 0
        score += self.conformity_to_scale(motif, mode)
        score += self.melodic_interest(motif, mode)
        score += self.rhythmic_complexity(motif)
        score += self.motivic_development_potential(motif)
        score += self.repetition_and_variation(motif)
        return score

    # Checks how many notes in the motif conform to the chosen musical mode
    '''
    Imagine a motif 'YYNYYN' and a mode that corresponds to a
    C major scale [60, 62, 64, 65, 67, 69]. 
    The function pairs each character of the motif with a note: 
    [('Y', 60), ('Y', 62), ('N', 64), ('Y', 65), ('Y', 67), ('N', 69)]. 
    It will count a '1' for each 'Y' that is paired with a note in the C major scale.
    '''

    def conformity_to_scale(self, motif, mode):
        scale_notes = set(self.modes[mode])
        return sum(1 for char, note in zip(motif, scale_notes) if char == 'Y' and note in scale_notes)

    # Assesses the melodic structure by comparing steps and leaps.
    def melodic_interest(self, motif, mode):
        leaps = 0
        steps = 0
        prev_note = None
        scale = self.modes[mode]
        # The for loop iterates over the motif,
        # pairing each character (char) with the corresponding note (note) from the scale.
        for char, note in zip(motif, scale):
            # differentiate between small melodic movements (steps) and larger ones (leaps).
            if char == 'Y' and prev_note is not None:
                # The interval represents the melodic distance between two consecutive notes.
                interval = abs(note - prev_note)
                # If the interval is greater than 2, it is considered a leap,
                # and the leaps counter is incremented.
                if interval > 2:
                    leaps += 1
                else:
                    steps += 1
            # This approach encourages a balance
            # in the motif between stepwise motion and larger intervals,
            # contributing to melodic interest.
            prev_note = note if char == 'Y' else prev_note

        return min(leaps, steps)

    # Evaluates the rhythmic diversity in the motif
    def rhythmic_complexity(self, motif):
        '''
        This line of code computes the rhythmic variety present in the motif.
        set(motif) converts the motif into a set. A set is a collection of unique elements, 
        so duplicate characters ('Y's and 'N's) in the motif are counted only once.
        len(set(motif)) then counts the number of unique elements in the set. 
        Since the motif can only contain 'Y' and 'N', the maximum possible count is 2 (one 'Y' and one 'N').
        '''
        rhythmic_variety = len(set(motif))
        '''
        The function then subtracts 1 from the count of unique rhythmic elements.
        The idea behind subtracting 1 is to normalize the score:
        If the motif has no variety (i.e., all 'Y's or all 'N's), 
        the score will be 0 (1 unique element - 1).
        If the motif contains both 'Y' and 'N', indicating rhythmic variety, 
        the score will be 1 (2 unique elements - 1).
        '''
        return rhythmic_variety - 1

    # Checks if the motif contains both notes and rests
    def motivic_development_potential(self, motif):
        '''
        If both conditions are true, which means the motif contains both notes and rests, 
        the function returns 1. This indicates that the motif has potential for motivic development. 
        The presence of both notes and rests suggests that the motif has a mix of sound and silence, 
        which can be a basis for further musical development.
        If either condition is false (meaning the motif contains all notes or all rests), 
        the function returns 0. This indicates a lack of motivic development potential, 
        as the motif lacks either rhythmic variation or melodic content.
        '''
        return 1 if 'Y' in motif and 'N' in motif else 0

    # Rewards motifs with a balance between repetition and variation
    def repetition_and_variation(self, motif):
        # counts the number of unique elements (characters) in the set.
        # Since the motif can contain 'Y' and 'N',
        # this count reflects the variety in the motif's composition.
        # set removes any duplicate characters in the motif.
        unique_elements = len(set(motif))
        # It checks if the number of unique elements is between 2 and 4 (inclusive).
        # If so, the motif is considered to have a good balance and the function returns 1.
        # If the number of unique elements is less than 2 or more than 4,
        # it is considered either too repetitive or too varied, and the function returns 0.
        return 1 if 2 <= unique_elements <= 4 else 0

    # Selects the top half of the population based on fitness scores for breeding
    def select_parents(self, population):
        # sorts the entire population based on their fitness scores,
        '''
        population is list of motifs
        key=self.fitness_function specifies that the sorting should be based on the values returned 
        by the fitness_function for each motif in the population.
        reverse=True means the sorting is done in descending order, so motifs with higher fitness scores come first.
        '''
        sorted_population = sorted(
            population, key=self.fitness_function, reverse=True)
        # After sorting, the function selects the top half of
        # this sorted list to act as parents for the next generation.
        return sorted_population[:len(sorted_population)//2]

    # key component of the genetic algorithm,
    # specifically in the phase of generating new offspring (motifs) from existing ones (parents)
    # This function combines parts of two parent motifs to create a new motif,
    # mimicking the biological process of crossover in genetics
    def crossover(self, parent1, parent2):
        '''
        parent1 and parent2 are strings of the same length, 
        consisting of characters 'Y' and 'N', 
        where each character represents the presence or absence of a note.
        '''
        # selects a random point within the motif, which will be the crossover point.
        # generates a random integer that falls between 1 and the length of parent1 minus 1.
        # This ensures that the crossover point is within the bounds of the motif
        # and that it's not at the very beginning or end (which would result in simply copying one parent).
        crossover_point = random.randint(1, len(parent1) - 1)
        '''
        parent1[:crossover_point] takes the segment of parent1 from the beginning up to (but not including) the crossover point.
        parent2[crossover_point:] takes the segment of parent2 from the crossover point to the end.
        These two segments are then concatenated (+) to form a new motif.
        '''
        return parent1[:crossover_point] + parent2[crossover_point:]

    # Introduces random changes to a motif,
    # with a higher chance of turning 'N' to 'Y' for notes in the scale
    '''
    motif: A string representing a musical motif, with each character being 'Y' (note played) or 'N' (no note played).
    mode: The musical mode (scale) that the motif is based on.
    generation: The current generation number in the genetic algorithm process.
    max_generations: The maximum number of generations that the algorithm will run
    '''

    def mutate(self, motif, mode, generation, max_generations):
        # This line randomly selects an index in the motif where the mutation will occur.
        mutation_point = random.randint(0, len(motif) - 1)
        # which note from the scale (defined by mode) corresponds to the mutation point.
        # The % operator ensures that the index wraps around if it exceeds the length of the scale.
        note = self.modes[mode][mutation_point % len(self.modes[mode])]
        # retrieves the list of preferred notes for the given mode.
        # If the mode isn't in self.preferred_notes, an empty list is used.
        preferred_notes = self.preferred_notes[mode] if mode in self.preferred_notes else [
        ]

        # Gradually increase the chance of preferred notes being 'Y'
        if note in preferred_notes:
            # calculates a threshold probability that changes based on the generation number.
            # Early generations have a lower threshold,
            # while later generations have a higher one, up to a maximum of 0.6.
            threshold = 0.3 + (generation / max_generations) * \
                0.3  # Adjust the range as needed
            # decides whether to mutate the character to 'Y' or 'N' based on this threshold.
            mutated_char = 'Y' if random.random() < threshold else 'N'
        else:
            # If the note is not preferred, the character at the mutation point is simply toggled from 'Y' to 'N' or vice versa.
            mutated_char = 'Y' if motif[mutation_point] == 'N' else 'N'
        # reconstructs the motif by combining the unaltered part before the mutation point,
        # the mutated character, and the unaltered part after the mutation point.
        return motif[:mutation_point] + mutated_char + motif[mutation_point + 1:]

    # Generates a new population from the current one using selection, crossover, and mutation.
    def generate_next_generation(self, current_generation):
        # select a subset of the current generation that will act as parents
        # for creating the next generation. The method typically selects
        # the fittest individuals based on their fitness scores.
        parents = self.select_parents(current_generation)
        #  store the motifs of the next generation
        next_generation = []
        # continues to generate new motifs until the next generation's size equals the current generation's size.
        # This ensures that the population size remains constant across generations.
        while len(next_generation) < len(current_generation):
            # Two parents are randomly selected from the parents list to create a new motif.
            # ensures that the same parent is not selected twice.
            parent1, parent2 = random.sample(parents, 2)
            #  called with the two parents to create a new motif (child).
            # This method combines parts of the parent motifs,
            # usually by splitting and recombining their strings at a random point.
            child = self.crossover(parent1, parent2)
            # This introduces small random changes to the motif,
            # which is crucial for maintaining genetic diversity
            # and exploring new possibilities in the motif space.
            child = self.mutate(child)
            next_generation.append(child)
        return next_generation

    # Runs the genetic algorithm for a number of generations, evolving the motifs
    '''
    generations: The total number of generations for which the genetic algorithm will run.
    population_size: The size of the population (number of motifs) to be maintained across generations.
    '''

    def run_genetic_algorithm(self, generations, population_size):
        # random musical mode from the self.modes dictionary.
        # This mode will be used to evaluate and generate motifs throughout the algorithm.
        mode = random.choice(list(self.modes.keys()))
        # creates a list of motifs, each of which is a string of 'Y' (note played) and 'N' (no note played).
        population = self.generate_initial_population(population_size, mode)

        # loop iterates through the specified number of generations.
        # Each iteration represents a new generation in the evolutionary process.
        for generation in range(generations):
            # he population is evaluated and sorted based on their fitness scores,
            # as determined by the fitness_function. The motifs are sorted in descending order,
            # with the fittest motifs at the front.
            population = sorted(population, key=lambda motif: self.fitness_function(
                motif, mode), reverse=True)

            # Selection: Keep the top half of the population
            # The top half of the sorted population is selected to be parents for the next generation.
            # This selection process favors motifs with higher fitness scores
            top_half = population[:len(population) // 2]

            # Crossover and mutation to create the next generation
            next_generation = top_half[:]
            while len(next_generation) < population_size:
                # Two parents are selected randomly from the top half
                parent1, parent2 = random.sample(top_half, 2)
                # A child motif is created
                child = self.crossover(parent1, parent2)
                # Mutation considering the mode and generation
                # The mutation is influenced by the current generation number
                # and the total number of generations, allowing for dynamic mutation rates.
                child = self.mutate(child, mode, generation, generations)
                next_generation.append(child)

            population = next_generation
        # This population represents the evolved motifs after undergoing multiple
        # rounds of selection, crossover, and mutation.
        return population

    # Converts a hexagram into a sequence of musical notes and rests based on the selected mode
    def hexagram_to_music(self, hexagram, mode):
        extended_scale = self.extended_modes[mode]
        music_sequences = []

        for _ in range(3):  # Creating 3 parts for polyphony
            sequence = []

            for i, char in enumerate(hexagram):
                note_duration = self.determine_note_duration(i, char)
                if char == 'Y':
                    # Randomly select a note from the extended range
                    selected_note = random.choice(extended_scale)
                    sequence.append((selected_note, note_duration))

                else:
                    sequence.append((None, note_duration))  # Rests
            music_sequences.append(sequence)

        return music_sequences

    def determine_note_duration(self, position, char):
        base_duration = 4
        if char == 'Y':
            # Introduce more variation in note durations
            return base_duration * random.choice([1, 1.5, 2])
        else:
            return base_duration * random.choice([0.5, 0.75, 1])

    def create_music21_score(self, music_sequences):
        score = stream.Score()
        score.metadata = metadata.Metadata(title="Hexagram Music Composition")

        for i, sequence in enumerate(music_sequences):
            part = stream.Part()
            part.id = f'Part {i+1}'
            for note_pitch, duration in sequence:
                if note_pitch is not None:
                    n = note.Note(note_pitch)
                    n.duration.quarterLength = duration
                    part.append(n)
                else:
                    r = note.Rest()
                    r.duration.quarterLength = duration
                    part.append(r)
            score.append(part)
        return score

    # Save the score as a MIDI file
    def save_as_midi(self, music_sequences, filename="hexagram_music.mid"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        midi_dir = "midi_generation"
        os.makedirs(midi_dir, exist_ok=True)
        midi_path = os.path.join(midi_dir, f"{timestamp}_{filename}")
        score = self.create_music21_score(music_sequences)
        score.write('midi', fp=midi_path)
        print(f"MIDI file saved as {midi_path}")

# Main


def main():
    gm = GeneticMusic()
    # run for 50 generations with a population size of 30 motifs
    final_motifs = gm.run_genetic_algorithm(
        generations=50, population_size=30)
    # musical mode is randomly selected from the available modes
    mode = random.choice(list(gm.modes.keys()))

    for motif in final_motifs:
        music_sequences = gm.hexagram_to_music(motif, mode)
        gm.save_as_midi(music_sequences, f"motif_{motif}.mid")


if __name__ == "__main__":
    main()
