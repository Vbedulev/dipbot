SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `bottest`
--

-- --------------------------------------------------------

--
-- Структура таблицы `cars`
--

CREATE TABLE `cars` (
  `idDriver` int(11) NOT NULL,
  `name` text NOT NULL,
  `gosNom` text NOT NULL,
  `lastTO` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `cars`
--

INSERT INTO `cars` (`idDriver`, `name`, `gosNom`, `lastTO`) VALUES
(321058459, 'LADA Granta', 'x111xx11', '2020-05-01');

-- --------------------------------------------------------

--
-- Структура таблицы `docs`
--

CREATE TABLE `docs` (
  `id` int(11) NOT NULL,
  `idDriver` int(11) NOT NULL,
  `name` text NOT NULL,
  `tgID` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `docs`
--

INSERT INTO `docs` (`id`, `idDriver`, `name`, `tgID`) VALUES
(7, 321058458, '1.txt', 'BQACAgIAAxkBAAICE17Cs_XExw40KUeqhW-CJ-dEnlsgAALeBgACrtEZSmqcPHBpZyxJGQQ'),
(8, 321058457, '1.txt', 'BQACAgIAAxkBAAICGF7Cs__yMfJBs-dcYgKpooyH6LZHAALfBgACrtEZSvqvAZG9VZB9GQQ'),
(9, 321058458, '1 (2).txt', 'BQACAgIAAxkBAAICHV7CtB5zvWyJ1E445gKVGI325-plAALgBgACrtEZSoR53xIp4QzxGQQ'),
(10, 321058457, '4654796879654.txt', 'BQACAgIAAxkBAAICZF7CtNY8IhLilSvBgkDidZMwApjMAALmBgACrtEZSp70skzJiddNGQQ'),
(12, 321058458, 'sample.fxml', 'BQACAgIAAxkBAAICnl7CtuVzndyyntmZ5rDni7XTIZWGAAKABgACp0sYSknAgC1gW1KsGQQ');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL,
  `groupmember` int(11) NOT NULL,
  `Contacts` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`id`, `name`, `groupmember`, `Contacts`) VALUES
(11, 'Тест Тест Тест', 2, '+79020785956'),
(120304722, 'Иванов Виталий Витальевич', 2, '79126094103'),
(321058457, 'Иванов Иван2', 3, '+7960'),
(321058458, 'Иванов Иван', 3, '+7960'),
(321058459, 'Тест Тест Тест2', 3, '+79627416182'),
(1158118462, 'Тест Тест Тест111', 2, '+79020785956');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `cars`
--
ALTER TABLE `cars`
  ADD UNIQUE KEY `gosNom` (`gosNom`(999));

--
-- Индексы таблицы `docs`
--
ALTER TABLE `docs`
  ADD UNIQUE KEY `idDoc` (`id`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD UNIQUE KEY `id` (`id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `docs`
--
ALTER TABLE `docs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
