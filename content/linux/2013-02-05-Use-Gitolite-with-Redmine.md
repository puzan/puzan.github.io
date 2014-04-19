Title: Использование Gitolite вместе с Redmine
Tags: git, redmine, gitolite

Появилась необходимость  добавить git репозиторий в  *[Redmine][redmine]* проект
на   домашнем    сервере.    Для   управления   git    репозиториями   использую
*[Gitolite][gitolite]*. Как  оказалось по-умолчанию *Gitolite*  запрещает доступ
всем кроме  пользователя, которым  он обслуживается. В  моем случае  доступ есть
только у пользователя *`git`*.  *Redmine* же запускает пользователь *`redmine`*.
В общем главная загвоздка — найти *umask* опцию в настройках *Gitolite*.

Решение со [Stackoverflow][stack]:

* Добавляем   в   Redmine   путь    к   необходимому   репозиторию.    Например:
  `/home/git/repositories/repo.git`.
* Добавить   пользователя,   который   запускает  веб-сервер   с   *Redmine*   в
  *`git`*-группу:
  
          usermod -a -G git redmine

* В  файле `.gitolite.rc`  (находится  в домашней  директории *`git`*)  поменять
  значение  `UMASK` с  `0077` на  `0027`.  Теперь  новые файлы  *Gitolite* будет
  создавать с правами на чтение для группы *`git`*.
* Также необходимо поменять права доступа  для всех существующих репозиториев. В
  директории с репозиториями запускаем следующее:
  
          chmod -R g+rX

Есть еще варианты решения этого вопроса?

[redmine]: http://www.redmine.org
[gitolite]: https://github.com/sitaramc/gitolite
[stack]: http://stackoverflow.com/questions/13000247/redmine-gitolite-issue-with-repository-permissions-and-more

