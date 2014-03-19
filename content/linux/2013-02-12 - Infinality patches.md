Title: Infinality патчи на стабильной ветке
Tags: gentoo, infinality, fonts

Как-то  я пропустил  тот  факт,  что похоже  уже  давно [infinality][inf]  патчи
находятся  на  стабильной  ветке  в  gentoo portage.   До  этого  ставил  их  из
[lcd-filtering][lcd].   Теперь все  намного  [проще][link].  Добавляем  USE-флаг
`infinality` в `make.conf` и пересобираем *freetype*:

    emerge -1q freetype
    eselect fontconfig enable 52-infinality.conf
    eselect infinality set infinality
    eselect lcdfilter set infinality

Как видим теперь необходимо несколько раз дополнительно запустить `eselect`. При
этом   вариантов  для   выбора  `eselect   infinality`  и   `eselect  lcdfilter`
предоставляют многовато.   Я с  ними не  экспериментировал.  Если  кто пробовал,
поделитесь впечатлениями.

[link]: http://od-eon.com/blogs/stefan/improving-the-font-rendering-on-gentoo-infinality/
[lcd]: http://gitorious.org/lcd-filtering
[inf]: http://www.infinality.net/blog/
