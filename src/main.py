from textnode import TextNode, TextType

def main():
    node = TextNode("foo bar baz", TextType.BOLD, "https://www.voylento.com") 
    print(f"{str(node)}")

if __name__=="__main__":
    main()
