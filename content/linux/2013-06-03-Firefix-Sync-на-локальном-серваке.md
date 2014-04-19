Title: Личный Firefox Sync
Tags: firefox, gentoo, portage, ebuild

Для синхронизации браузерной  информации я использую *Firefox  Sync*.  Но совсем
недавно замучили проблемы синхронизации. Постоянно появлялась ошибка, что сервер
не доступен, хотя  на сайте [mozilla][sync-status] не было  сообщений о каких-то
ошибках и неполадках в работе сервиса. Сейчас кстати есть:

> The  Firefox  Sync  service  is  undergoing  some  load  issues,  if  you  are
> experiencing problems  please wait and  try again soon.  We are working  on it
> presently.

Помучившись так  недельку, я решил поднять  личный Firefox Sync сервер  на своем
псевдо сервере. Быстренько нашел [ebuild'ы][ebuild]  для *gentoo*.  И, вуа-ля, у
меня рабочий  сервер для синхронизации. Еще  я написал *init* скрипты  и выложил
свой [overlay  на github][puzan-overlay].  Если  кому-то нужно —  пользуйтесь на
здоровье.

Плюсы которые обнаружил во время использования личного Firefox Sync сервера:

* Нет проблем с  доступом, точнее их я  могу решить сам.  Более того,  так как я
  единственный пользователь своего сервера, то  нет проблем с загруженностью.  А
  вот доступной  поддержки для  Firefox Sync  не нашел.   Признаюсь не  сильно и
  искал.
* Фактически  нет  ограничения  на  размер  хранимых  данных.  Стандартный  5-ти
  мегабайтный предел я умудрился превысить.

[sync-status]: https://services.mozilla.com/status/
[ebuild]: http://gpo.zugaina.org/Search?search=mozilla-sync-server
[puzan-overlay]: https://github.com/puzan/puzan-overlay
