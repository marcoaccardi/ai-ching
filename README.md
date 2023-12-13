## AI-CHING
[presentation](https://docs.google.com/presentation/d/1wSeUJE2EYxV_REA8xXIxVVzF6P0pRR2fOopGCzstfs4/edit?usp=sharing)
[hexagram_rules](https://www.lovetoknow.com/home/design-decor/i-ching-hexagrams)



### SUMMARY
This code represents a creative application of genetic algorithms to music composition. Each motif, represented as a combination of 'Y' and 'N', undergoes evolution through genetic operations like selection, crossover, and mutation. The fitness function, which evaluates these motifs, is based on various musical criteria. The final motifs are then translated into music sequences, demonstrating how abstract genetic information can be transformed into actual music. The use of music21 allows for the conversion of these sequences into MIDI files, making the compositions audible.

## ABOUT THE CODE
**Class GeneticMusic**
Initialization (__init__):

self.hexagrams: Creates all possible combinations of 6-character strings made of 'Y' and 'N'.
self.modes: Defines musical modes (scales) with specific MIDI note numbers.
self.extended_modes: Expands each mode with notes from two octaves down and the original octave.
self.preferred_notes: Specifies preferred notes for each mode.
Population Generation (generate_initial_population):

Generates an initial population of motifs (hexagrams) based on a specified musical mode. Each motif is a 6-character string ('Y' or 'N'), representing the presence or absence of a note.
Fitness Function (fitness_function):

Evaluates a motif's fitness based on multiple musical factors, including conformity to scale, melodic interest, rhythmic complexity, motivic development potential, and repetition/variation.
Fitness Components:

conformity_to_scale: Checks how many notes in the motif conform to the chosen musical mode.
melodic_interest: Assesses melodic structure by comparing steps and leaps between notes.
rhythmic_complexity: Evaluates rhythmic diversity in the motif.
motivic_development_potential: Checks if the motif contains both notes and rests.
repetition_and_variation: Rewards motifs with a balance between repetition and variation.
Parent Selection (select_parents):

Selects the top half of the population based on fitness scores for breeding.
Crossover (crossover):

Combines two motifs to create a new one.
Mutation (mutate):

Introduces random changes to a motif. The mutation rate changes over generations, especially for preferred notes.
Next Generation (generate_next_generation):

Generates a new population using selection, crossover, and mutation.
Run Algorithm (run_genetic_algorithm):

Runs the genetic algorithm over a specified number of generations, evolving the motifs.
Music Generation (hexagram_to_music):

Converts a hexagram into a sequence of musical notes and rests based on the selected mode.
Music21 Score Creation (create_music21_score):

Converts the musical sequences into a music21 score.
MIDI File Saving (save_as_midi):

Saves the music21 score as a MIDI file.

**Main Function**
Creates an instance of GeneticMusic.
Runs the genetic algorithm to generate final motifs.
Converts each motif into a musical sequence and saves it as a MIDI file.


### CONFORMITY TO SCALE
The conformity_to_scale function is a way to numerically evaluate how well a musical motif adheres to a particular scale. This is a crucial part of the genetic algorithm in this context, as it quantifies an aspect of the motif's musicality—its harmonic alignment with a chosen scale. Tweaking this function or the scales in self.modes can lead to different interpretations of what constitutes a harmonically 'fit' motif.

### MELODIC INTEREST
The melodic_interest function provides a way to numerically assess the melodic composition of a motif. By counting steps and leaps, it evaluates how the motif moves melodically. This function favors motifs that have a balance between stepwise movements and larger leaps, as this is often seen as more musically interesting.

To **adjust** this function for different musical preferences, you might:
Change the threshold that defines a leap.
Modify the function to give different weights to leaps and steps.
Adjust the balance criterion, for instance, favoring either more leaps or more steps, depending on your musical objectives.

### RHYTHMIC COMPLEXITY 
The rhythmic_complexity function provides a simple way to quantify the rhythmic diversity in a motif. A motif with both notes and rests ('Y' and 'N') will have a higher rhythmic complexity score (1) than a motif with no rhythmic variety (0).

**Possible Adjustments**
Expand Rhythmic Elements: If the motif were to include more rhythmic elements (like different types of rests or note durations), the function could be adapted to count these additional elements, leading to a potentially higher rhythmic complexity score.
Different Scoring Logic: The way the score is calculated (subtracting 1) is quite basic. Depending on the desired complexity, you might adjust the scoring logic to better reflect the rhythmic intricacies you want to capture.

### MOTIVIC DEVELOPMENT
The motivic_development_potential function provides a binary assessment (1 or 0) of whether a motif has the basic elements (notes and rests) that could lead to more interesting and complex musical development. This assessment is based on the presence of both 'Y' and 'N' characters in the motif.

**Possible Adjustments**
More Complex Criteria: If desired, this function could be modified to include more sophisticated criteria for assessing development potential. For example, it could take into account the length of notes and rests, their distribution, or other aspects of musical composition.
Different Representations of Notes/Rests: If the representation of motifs is expanded beyond just 'Y' and 'N' (for example, to include different types of notes or varying rest lengths), the function could be adapted to account for these additional complexities.


### REPETITION AND VARIATIONS
The repetition_and_variation function is a simple way to quantify and encourage a balance between repetition and variation within a motif. This balance is often crucial in music composition, as it contributes to the musicality and interest of a piece.

**Possible Adjustments**
Adjusting the Range: The range of 2 to 4 unique elements can be adjusted depending on what is considered an ideal balance in the specific musical context.
Expanding Motif Representation: If the representation of motifs is expanded beyond 'Y' and 'N', this function could be adapted to account for a wider range of musical elements, thereby allowing for a more nuanced assessment of repetition and variation.

### SELECT PARENTS
The select_parents function in the GeneticMusic class is a crucial part of the genetic algorithm, specifically in the selection phase. Its role is to select a subset of the current population to act as parents for the next generation.

The select_parents function implements a common selection strategy in genetic algorithms known as "truncation selection." In this approach, only a certain percentage of the fittest individuals (in this case, the top 50%) are selected to reproduce. This method is straightforward and effective at pushing the population towards better fitness over successive generations.

**Possible Adjustments**
Selection Proportion: You might adjust the proportion of the population that is selected as parents. Instead of taking the top 50%, you could try taking a different percentage to see how it affects the evolution of motifs.
Different Selection Strategies: There are other selection methods like roulette wheel selection, tournament selection, or rank-based selection that you could implement to see how they impact the genetic algorithm's performance. Each method has its own way of balancing the exploration and exploitation in the search for optimal solutions.

### CROSSOVER
The crossover function combines segments from two parent motifs to create a new motif. This is a fundamental process in genetic algorithms, as it allows for the mixing of genetic material (in this case, motif patterns) from two parents, potentially leading to new and favorable combinations in the offspring.

**Possible Adjustments**
Crossover Technique: The single-point crossover used here is just one method. You could experiment with other crossover techniques like two-point crossover (where two points are chosen, and the segments between these points are swapped) or uniform crossover (where each character is independently chosen from one of the two parents).
Crossover Probability: In some implementations, crossover is not always performed; instead, it's done based on a certain probability. This introduces another layer of randomness and can help maintain diversity in the population.

### MUTATE
The mutate function introduces random changes to a motif, with a special consideration for preferred notes in the given musical mode. The probability of mutating to a preferred note increases as the algorithm progresses through generations. This mechanism not only introduces variability but also steers the evolution of motifs towards musically favorable patterns as defined by the preferred notes of the mode.

**Possible Adjustments**
Mutation Rate: You might experiment with different ways of adjusting the mutation rate or threshold, possibly making it depend on other factors or introducing more randomness.
Mutation Logic: The way preferred notes are treated can be altered, or additional rules for mutation can be introduced, depending on the desired musical outcomes.


## GENERATE NEXT GENERATION
generate_next_generation function is central to the genetic algorithm's iterative process. It ensures the continuation of the population from one generation to the next, applying genetic operations like selection, crossover, and mutation. This process allows the algorithm to explore the space of potential solutions (in this case, musical motifs) and evolve towards more optimal motifs over time.

**Possible Adjustments**
Crossover and Mutation Rates: You might introduce probabilities for crossover and mutation, so they don't always occur for every child. This can introduce additional variability into the process.
Different Selection Strategies: The method of selecting parents can be varied. For instance, you might try different selection techniques to see how they affect the evolution of the motifs.
Tuning the Genetic Operations: The specific mechanisms of crossover and mutate can be adjusted or entirely new methods can be introduced to influence the evolution process in different ways.

## HEXAGRAM TO MUSIC
The hexagram_to_music function transforms a hexagram motif into a set of music sequences, each representing a part in a polyphonic piece. It uses a mix of random selection and algorithmic conversion to turn the abstract pattern of 'Y' and 'N' characters into concrete musical elements like notes and rests, considering their durations and positions in the scale. This process is crucial for realizing the genetic algorithm's output as audible music.

## MAIN
main function in this code serves as the entry point for running a music generation process using a genetic algorithm. It orchestrates the creation, evolution, and conversion of musical motifs into MIDI files.