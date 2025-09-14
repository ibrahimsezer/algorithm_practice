# This script finds the frequency of words in a given text.

# Step 1: Define the comments and stop words.
# We can populate this list with real-world data.
comments = [
    "this product is a great product",
    "the service is very good",
    "product quality is very good",
    "great service"
]

# Stop words are words that are generally ignored in text analysis.
stop_words = ["this", "is", "a", "the", "very"]

# Step 2: Create an empty dictionary to store word counts.
# We will store the word as the key and its frequency as the value.
word_counts = {}

# Step 3: Write the function to process the text.
# This function takes a string, converts it to lowercase, removes punctuation,
# and splits it into a list of words.
def process_text(text):
    # Convert the text to lowercase.
    text = text.lower()

    # Remove punctuation.
    cleaned_text = ""
    for char in text:
        if 'a' <= char <= 'z' or char == ' ':
            cleaned_text += char

    # Split the cleaned text into a list of words.
    return cleaned_text.split()

# Now, let's proceed with the main algorithm.
# Iterate through each comment in the comments list.
for comment in comments:
    # Process the comment to get a list of words.
    words = process_text(comment)

    # Iterate through each word in the list of words.
    for word in words:
        # Check if the word is not in the set of stop words for efficient lookup.
        if word not in set(stop_words):
            # If the word is not in the dictionary, add it with a value of 1.
            if word not in word_counts:
                word_counts[word] = 1
            # If the word is already in the dictionary, increment its count.
            else:
                word_counts[word] += 1

# Step 4: Print the results to the screen.
print("Word frequencies:")
print(word_counts)
