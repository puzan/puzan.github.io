Title: Linux бекапы на Apple Time Capsule (Obnam)
Tags: linux, apple, time capsule, cifs, obnam, backup

Решил наладить  бекапы с *CubieBoard*,  на которой крутится  подточеный *Debian*
([*Cubian*][cubian]), на *Time Capsule*.  Туда через *Time Machine* уже делается
резервная копия  *MacBook*'а.  Захотел организовать  аналогичные инкрементальные
бекапы для *Linux* коробки. Попытаюсь далее изложить свой опыт.

С  доступом  к  *Time  Capsule*  особых   проблем  в  *Linux*  нету.   Ее  можно
подмонтировать с помощью *cifs* (не забываем установить `cifs-utils`). В `fstab`
закидываем следующую строку и все должно работать после монтирования.

    //<TC.local or direct ip>/Data /mnt/tc cifs passwd=thebestpass,sec=ntlm,iocharset=utf8 0 0

Но при этом в `/var/log/messages` порой валит вот такие ошибки:

```
[151119.364105] ------------[ cut here ]------------
[151119.375676] WARNING: at fs/inode.c:280 drop_nlink+0x54/0x5c()
[151119.380041] Modules linked in: sunxi_cedar_mod mali ump gpio_sunxi
[151119.394514] [<c0015430>] (unwind_backtrace+0x0/0x134) from [<c003322c>] (warn_slowpath_common+0x54/0x64)
[151119.403340] [<c003322c>] (warn_slowpath_common+0x54/0x64) from [<c00332d8>] (warn_slowpath_null+0x1c/0x24)
[151119.411578] [<c00332d8>] (warn_slowpath_null+0x1c/0x24) from [<c00f0738>] (drop_nlink+0x54/0x5c)
[151119.419177] [<c00f0738>] (drop_nlink+0x54/0x5c) from [<c0248cfc>] (cifs_unlink+0x224/0x654)
[151119.426644] [<c0248cfc>] (cifs_unlink+0x224/0x654) from [<c00e64d0>] (vfs_unlink+0x78/0x104)
[151119.434358] [<c00e64d0>] (vfs_unlink+0x78/0x104) from [<c00e66a0>] (do_unlinkat+0x144/0x16c)
[151119.447019] [<c00e66a0>] (do_unlinkat+0x144/0x16c) from [<c000ec40>] (ret_fast_syscall+0x0/0x30)
[151119.451059] ---[ end trace fddecabeb4cc4bce ]---
```

Вроде ничего страшного, но логи забиваются.

Далее стоит вопрос,  чем и как бекапить.  Для *Linux*  популярны системы бекапов
на  основе `rsync`  и *hard  links*.  Например,  [rsnapshot][rsnapshot]. Но  тут
возникает проблема, связанная  с отсутствием поддержки жестких  ссылок в *cifs*.
Есть еще [rdiff-backup][rdiff-backup], он вроде  как хранит файлы с изменениями.
Но это мой  следующий шаг для тестов, а пока  я использую [**obnam**][obnam].  И
сразу скажу: он очень тормозной.

На **obnam**  натолкнулся когда-то  [давно][obnam-news], но  начал разворачивать
после приобретения *CubieBoard*.  Первоначально  **obnam** мне очень понравился.
Гигабайт системных данных бекапил минуты за  2-3.  Я с радости поднял ежечастные
бекапы.  Вроде как настроил систему  аналогичную *Time Capsule* c чисткой старых
поколений бекапов (см. поле `keep` в  настройках ниже).  Для всего этого написал
небольшой скрипт следующего содержания и положил это добро в крон:

```shell
#!/bin/sh

logger "Start backup"

if ! (df | tail -n +2 | awk '{print $6}' | grep -q '^/mnt/tc$')
then
    logger "Backup fails: tc is not mounted"
    exit 1
fi

nice -n 19 ionice -c2 -n7 obnam backup

if [ $? -eq 0 ]
then
    logger "Backup forget"
    nice -n 19 ionice -c2 -n7 obnam forget
else
    logger "Backup failed"
fi

logger "End backup"
```

А вот и **obnam** конфиг:

```
[config]
repository = /mnt/tc/backup
log = /var/log/obnam.log
log-max = 10M
log-keep = 10
log-level = warning
one-file-system = True
root = /etc, /home, /opt, /root
keep = 24h,7d,15w,24m,5y
upload-queue-size = 512
lru-size = 512
compress-with = deflate
```

Все это прекрасно  работало до того момента, как я  перенес [seafile][seafile] с
~100  гигабайтами данных.   Первичный  бекап занял  около  30 часов.   Следующие
занимали более часа.  К сожалению  подробную статистику не сохранил. После этого
нашел [пост][obnam-performance], посвященный  тестированию **obnam** параметров,
влияющих  на  производительность.  На  основе  информации  из указанной  заметки
добавил параметры `upload-queue-size`  и `lru-size` в конфиг  (см.  выше). Бекап
ускорился до 15 минут.

Но далее я обновил *seafile* через несколько версий, и вдруг количество файлов в
его базе увеличилось  примерно в 2-е (в основном жестки  ссылки).  Это привело к
росту времени бекапов до 1 часа 15  минут.  Я боюсь представить за сколько будет
проходить бекап  почти забитого  1 Тб  диска.  Надеюсь у  меня не  будет столько
данных.  Соответственно бекапы теперь запускаются раз в день. Вроде бы этого для
меня вполне достаточно.

И  еще один  шаг, который  как  раз заканчиваю  тестировать: положить  **obnam**
репозиторий в [encfs][encfs]. Выбор на этот вариант шифрования также пал за счет
поддержки *cifs*. Также  *encfs* хороша тем, что нет  необходимости делать некий
виртуальный диск, который  возможно в будущем придется  расширять. Позже добавлю
информацию про эти успехи.

Данный пост  был создан,  чтобы поделиться собственным  опытом и  возможно найти
более эффективные альтернативы. Добро  покалывать в комментарии. Высказывайтесь!
**obnam** явно не  лучший вариант для бекапов больших  объемов информации поверх
*cifs*.

**P.S.**  К слову  сказать, бекапы  уже  меня успели  спасти. Пусть  они и  идут
медленно,  но  и  меняются  не сильно  часто.   После  выключения  электричества
файловая система  на диске с  данными слегка  поплыла.  Чиниться через  `fsck` и
монтироваться  отказывалась.  Данные  в принципе  можно было  бы восстановить  с
диска,  но  быстрее и  проще  оказалось  воспользоваться бекапом.   Бекаптесь  -
пригодится!

[obnam-news]: http://www.opennet.ru/opennews/art.shtml?num=39323
[cubian]: http://cubian.org/
[rsnapshot]: http://www.rsnapshot.org/
[rdiff-backup]: http://www.nongnu.org/rdiff-backup/
[obnam]: http://obnam.org/
[seafile]: http://seafile.com
[obnam-performance]: http://listmaster.pepperfish.net/pipermail/obnam-support-obnam.org/2014-June/003086.html
[encfs]: https://github.com/vgough/encfs
