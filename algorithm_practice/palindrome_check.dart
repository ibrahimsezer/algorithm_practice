class PalindromeCheck {

bool isPalindrome(String str){
  String cleaned = str.replaceAll(RegExp(r'[^a-zA-Z0-9]'), '').toLowerCase();
  String reversed = cleaned.split('').reversed.join('');
  return cleaned == reversed;

}}

void main() {
  PalindromeCheck checker = PalindromeCheck();
  print(checker.isPalindrome("A man, a plan, a canal: Panama")); // true
  print(checker.isPalindrome("race a car")); // false
}