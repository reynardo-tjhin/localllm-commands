import time

ID="c66d9421757f4051aa2f99b5305cb037"
NAME="Test Script 2"
DESCRIPTION="Script for Testing No 2"

def execute():
    
    print("test_script_2: started")
    
    with open("test.txt", "w") as f:
        f.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent aliquet erat metus. Etiam mattis placerat arcu, in vulputate purus tincidunt vitae. Ut vel tortor mattis ante elementum ornare eget sit amet nisi. Fusce quis quam nisi. Praesent ipsum justo, vehicula vitae accumsan quis, sagittis eu quam. Proin sollicitudin enim diam, id pellentesque arcu condimentum et. Nam nec vulputate nisi. Nunc id egestas ipsum. Etiam in turpis tellus. Etiam commodo nibh vitae nibh porttitor, non rhoncus nunc tempor. Praesent lacinia felis odio. Donec tincidunt est lobortis interdum hendrerit. Aliquam eros metus, mattis bibendum posuere in, suscipit sit amet dolor.\n\n")
        
        f.write("Nunc ac facilisis urna, in vulputate neque. In eu orci at purus congue accumsan. Donec dapibus justo quam, a suscipit dolor euismod a. Duis eget semper sapien. Vivamus sit amet ullamcorper est. Donec vehicula ipsum sem, ac placerat neque ultrices id. In tristique molestie leo, non ultrices velit consequat quis.\n\n")

        f.write("Proin ultricies dictum enim, id malesuada lectus placerat ac. Maecenas et sodales nulla. Morbi non augue eu leo faucibus pulvinar. Praesent ut scelerisque ipsum, eu aliquam leo. Aliquam consectetur nulla eleifend tellus viverra, quis gravida mauris tincidunt. Duis bibendum metus pellentesque pellentesque pulvinar. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam diam justo, egestas eu hendrerit et, vestibulum gravida nisi. Etiam rutrum mauris dui, at eleifend enim tristique vitae.\n\n")

        f.write("Cras eu elit in dolor blandit vestibulum a non neque. Maecenas feugiat ut dui hendrerit dignissim. Phasellus pretium mauris non mi euismod, nec mollis eros malesuada. Proin fringilla velit turpis, in laoreet enim hendrerit sit amet. Quisque convallis vestibulum enim vel sollicitudin. Morbi tempor nisi venenatis sem maximus, nec placerat leo consequat. Aliquam at viverra neque. Aliquam dapibus ipsum eget dui dictum molestie. Sed luctus nunc ac vulputate dignissim. Praesent sodales turpis dolor, nec rutrum felis pulvinar non. Etiam convallis purus vel porttitor venenatis. Vivamus egestas velit at pharetra sollicitudin. Curabitur in purus erat. Vestibulum tincidunt mi id dolor tempus, nec rutrum libero vestibulum.\n\n")

        f.write("Vivamus pharetra blandit aliquam. Suspendisse eu pharetra arcu, vel hendrerit ligula. Etiam eu ultrices felis. Proin in ligula pellentesque, tempus dui at, faucibus sem. Suspendisse potenti. Donec pharetra viverra nisi a laoreet. Proin tempus, lorem eu efficitur efficitur, elit orci tincidunt erat, sit amet sodales nulla ligula vel ipsum. Etiam condimentum sodales scelerisque. Aliquam dignissim leo sit amet bibendum sollicitudin. Etiam posuere finibus nulla in facilisis. In sit amet euismod turpis. Praesent volutpat metus sem, sed venenatis mauris mattis eu. Nam eleifend vulputate lectus, tempor faucibus tellus lobortis aliquam. Mauris sagittis rhoncus neque et consectetur.")
    
    return None
