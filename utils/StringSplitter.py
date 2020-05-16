import string


class StringSplitter:
    def __init__(self, text):
        self.string = text.lower()
        self.string_list = []
        self.bad = set()
        for punct in string.punctuation:
            if punct != "'" or punct != "-":
                self.bad.add(punct)
        for num in '1234567890':
            self.bad.add(num)

    def string_splitter(self, words_a_string):
        clean = self._strip_bad_chars()
        words = clean.split(' ')
        count = 0
        big_string = ''
        for i in range(len(words)):
            if count == words_a_string - 1:
                count = 0
                big_string += words[i]
                self.string_list.append(big_string)
                big_string = ''
            else:
                big_string += words[i] + " "
                count += 1

    def _strip_bad_chars(self):
        clean_string = ''
        for index in range(len(self.string)):
            if self.string[index] not in self.bad:
                clean_string += self.string[index]
        return clean_string

    def show_list(self):
        return self.string_list


if __name__ == "__main__":

    s = StringSplitter('Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed accumsan libero neque, nec viverra quam egestas in. Vivamus id egestas mauris, eu commodo arcu. Curabitur est eros, blandit quis nulla sed, viverra sodales risus. Sed in tellus porta, volutpat est ut, ullamcorper purus. Praesent tincidunt erat at dapibus aliquet. Maecenas et convallis lorem, vitae ultricies metus. Ut at quam ultrices, gravida mi non, vehicula urna. Quisque aliquet facilisis ligula, ut vestibulum dolor rhoncus sed. Quisque interdum lacus ut vulputate venenatis. In non turpis leo. Aenean id semper tortor, id rutrum neque. Fusce posuere, tortor non tristique luctus, velit turpis molestie augue, non eleifend sem tortor sed odio. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Donec quis erat in odio vulputate fringilla eget eu velit. Etiam eleifend dui est, porta commodo dui mollis vel.')
    s.string_splitter(10)
    print(s.show_list())
