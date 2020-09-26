# whatsapp_chat_emulation
Emulates Whatsapp chat screen in terminal using exported chats.

Just a fun project.

# In Action

![Alt text](in_action.png?raw=true "running under Artix Linux and dwm")

*running under Artix Linux and dwm*

**The corresponding exported chat:**

`11/09/20, 9:25 pm - Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them. Tap to learn more.

11/09/20, 9:25 pm - Andrew: Hey buddy! What's up?

11/09/20, 9:25 pm - John: I'm fine mate. How's you?

11/09/20, 9:25 pm - Andrew: Me too. 😊

11/09/20, 9:25 pm - John: Do you remember that car deal we were discussing about yesterday?

11/09/20, 9:25 pm - Andrew: Yeah! What about it?

11/09/20, 9:25 pm - John: Well, we're late. They sold it!

11/09/20, 9:26 pm - Andrew: Really? That's sad!
`

# Getting it running in your system
* must have python-3.x installed
* must have gobject-introspection-1.0
    
    name of the package depends on your distribution, e.g.

    Fedora, CentOS, RHEL: gobject-introspection-devel

    Debian, Ubuntu, Mint, Elementary: libgirepository1.0-dev

    ArchLinux: gobject-introspection

* must have PyGObject

    to install: `pip3 install PyGObject`

# USAGE
 `python chat.py -f path_to_file -p perspective`

# NOTES
As it's made in GTK and GTK is cross-platform, it should work fine in Windows and Mac. Try it yourself.

# LICENSE
Licensed under MIT License

*Copyright (c) 2020 Gaurav Kumar Yadav*

Have a look at the `LICENSE` for details