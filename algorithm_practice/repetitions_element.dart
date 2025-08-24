// This function takes a list and counts the occurrences of each unique element.
// It iterates through the list, and for each element not already counted,
// it compares it with the remaining elements to count duplicates.
// The element and its count are then added to a map.
// The process repeats for all unique elements, and the map is returned at the end.

class FindRepeatedElement {
  List arr = [2, 3, 2, 2, 1, 2, 3, 3, 4, 4, 4, 4];

  Map<dynamic, int> valueCounter(List get_arr) {
    Map<dynamic, int> dictionary = {};
    int counter = 1;

    for (int i = 0; i < get_arr.length; i++) {
      if (dictionary.keys.contains(get_arr[i])) {
        continue;
      }
      for (int j = i + 1; j < get_arr.length; j++) {
        if (get_arr[i] == get_arr[j]) {
          counter++;
        }
      }
      dictionary.addAll({get_arr[i]: counter});
      counter = 1;
    }

    return dictionary;
  }
}

class EfficientRepetitionFinder {
  List arr = [2, 4, 5, 5,5,5];
  Map<dynamic, int> dictionary = {};

  Map<dynamic, int> valueCounter(List get_arr) {
    for (int i = 0; i < get_arr.length; i++) {
      if (dictionary.containsKey(get_arr[i])) {
        dictionary.update(get_arr[i], (value) => value + 1);
      } else {
        dictionary.addAll({get_arr[i]: 1});
      }
    }
    return dictionary;
  }
}

void main() {
  FindRepeatedElement q1 = FindRepeatedElement();
  print(q1.valueCounter(q1.arr));
  EfficientRepetitionFinder q2 = EfficientRepetitionFinder();
  print(q2.valueCounter(q2.arr));
}
