CREATE TABLE Hero
(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    login VARCHAR(32) NOT NULL,
    password VARCHAR(64) NOT NULL,
    email VARCHAR(64) NOT NULL,
    experience INT(12) NOT NULL,
    money FLOAT(10, 2) NOT NULL,
    money_art FLOAT(10, 2) NOT NULL,
    location VARCHAR(32) NOT NULL,
    level INT(3) NOT NULL,
    image_id INT NOT NULL,

    number_of_wins INT(6) NOT NULL,
    number_of_losses INT(6) NOT NULL,
    number_of_draws INT(6) NOT NULL,

    hp INT(6) NOT NULL,

    strength INT(6) NOT NULL,
    dexterity INT(6) NOT NULL,
    intuition INT(6) NOT NULL,
    health INT(6) NOT NULL,

    swords INT(6) NOT NULL,
    axes INT(6) NOT NULL,
    knives INT(6) NOT NULL,
    clubs INT(6) NOT NULL,
    shields INT(6) NOT NULL,

    date_of_birthday DATE NOT NULL,
    sex INT(1) NOT NULL,
    country VARCHAR(32),
    city VARCHAR(32),
    name VARCHAR(64),
    about TEXT,

    feature_id INT NOT NULL,

    CONSTRAINT FK_hero_heroimage FOREIGN KEY (image_id)
        REFERENCES HeroImage (id) ON DELETE CASCADE ON UPDATE RESTRICT,

    CONSTRAINT FK_hero_herofeauture FOREIGN KEY (heature_id)
        REFERENCES HearoFeature (id) ON DELETE CASCADE ON UPDATE RESTRICT
);

CREATE TABLE HeroFeature
(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,

    strength VARCHAR(32),
    dexterity VARCHAR(32),
    intuition VARCHAR(32),
    health VARCHAR(32),

    swords VARCHAR(32),
    axes VARCHAR(32),
    knives VARCHAR(32),
    clubs VARCHAR(32),
    shields VARCHAR(32),

    protection_head VARCHAR(32),
    protection_breast VARCHAR(32),
    protection_zone VARCHAR(32),
    protection_leg VARCHAR(32),

    damage_min VARCHAR(32),
    damage_max VARCHAR(32),

    accuracy VARCHAR(32),
    dodge VARCHAR(32),
    devastate VARCHAR(32),
    durability VARCHAR(32),
    block_break VARCHAR(32),
    armor_break VARCHAR(32),

    hp VARCHAR(32),

    capacity VARCHAR(32),

    CONSTRAINT FK_herofeature_hero FOREIGN KEY (hero_id)
        REFERENCES Hero (id) ON DELETE CASCADE ON UPDATE RESTRICT
);

CREATE TABLE HeroImage
(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    image VARCHAR(32) NOT NULL,
    is_art BOOL NOT NULL,
    sex INT(1) NOT NULL,
);

CREATE TABLE HeroSkill
(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(32) NOT NULL
);

CREATE TABLE SkillFeature
(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    heroskill_id INT NOT NULL,
    feature INT(3) NOT NULL,
    plus INT(3) NOT NULL
);

CREATE TABLE HeroHeroSkill
(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    hero_id INT NOT NULL,
    skill_id INT NOT NULL,
    level INT(3) NOT NULL,
    CONSTRAINT FK_hero FOREIGN KEY (hero_id)
        REFERENCES Hero (id) ON DELETE CASCADE ON UPDATE RESTRICT,
    CONSTRAINT FK_heroskill FOREIGN KEY (skill_id)
        REFERENCES HeroSkill (id) ON DELETE CASCADE ON UPDATE RESTRICT
);

CREATE TABLE TableExperience
(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    level INT(3) NOT NULL,
    experience INT(12) NOT NULL,
    number_of_abilities INT(3) NOT NULL,
    number_of_skills INT(3) NOT NULL,
    number_of_parameters INT(3) NOT NULL,
    money INT(6) NOT NULL
);

CREATE TABLE Thing
(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(32) NOT NULL,
    type INT(3) NOT NULL,
    is_art INT(1) NOT NULL,
    is_bot INT(1) NOT NULL,
    stability INT(6) NOT NULL,
    image VARCHAR(32) NOT NULL,

    level_need INT(3) NOT NULL,

    strength_need INT(6) DEFAULT 0,
    dexterity_need INT(6) DEFAULT 0,
    intuition_need INT(6) DEFAULT 0,
    health_need INT(6) DEFAULT 0,

    swords_need INT(6) DEFAULT 0,
    axes_need INT(6) DEFAULT 0,
    knives_need INT(6) DEFAULT 0,
    clubs_need INT(6) DEFAULT 0,
    shields_need INT(6) DEFAULT 0,

    strength_give INT(6) DEFAULT 0,
    dexterity_give INT(6) DEFAULT 0,
    intuition_give INT(6) DEFAULT 0,
    health_give INT(6) DEFAULT 0,

    swords_give INT(6) DEFAULT 0,
    axes_give INT(6) DEFAULT 0,
    knives_give INT(6) DEFAULT 0,
    clubs_give INT(6) DEFAULT 0,
    shields_give INT(6) DEFAULT 0,

    damage_min INT(6) DEFAULT 0,
    damage_max INT(6) DEFAULT 0,

    protection_head INT(6) DEFAULT 0,
    protection_breast INT(6) DEFAULT 0,
    protection_zone INT(6) DEFAULT 0,
    protection_leg INT(6) DEFAULT 0,

    accuracy INT(6) DEFAULT 0,
    dodge INT(6) DEFAULT 0,
    devastate INT(6) DEFAULT 0,
    durability INT(6) DEFAULT 0,
    block_break INT(6) DEFAULT 0,
    armor_break INT(6) DEFAULT 0,

    hp INT(6) DEFAULT 0,

    time_duration INT(6) DEFAULT 0,

    strike_count INT(3) DEFAULT 0
);

CREATE TABLE HeroThing
(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    hero_id INT NOT NULL,
    thing_id INT NOT NULL,
    stability_all INT(6) NOT NULL,
    stability_left INT(6) NOT NULL,
    dressed INT(1) NOT NULL,

    CONSTRAINT FK_hero FOREIGN KEY (hero_id)
        REFERENCES Hero (id) ON DELETE CASCADE ON UPDATE RESTRICT,
    CONSTRAINT FK_thing FOREIGN KEY (thing_id)
        REFERENCES Thing (id) ON DELETE CASCADE ON UPDATE RESTRICT
);

CREATE TABLE HeroThingFeature
(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    herothing_id INT NOT NULL,
    feature INT(3) NOT NULL,
    plus INT(3) NOT NULL
);

CREATE TABLE Combat
(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    type INT(3) NOT NULL,
    is_active INT(1) NOT NULL,
    time_out INT(3) NOT NULL,
    injury INT(1) NOT NULL,
    with_things INT(1) NOT NULL,
    time_wait INT(3) NOT NULL,
    one_team_count INT(3),
    two_team_count INT(3),
    one_team_lvl_min INT(3),
    one_team_lvl_max INT(3),
    two_team_lvl_min INT(3),
    two_team_lvl_max INT(3),
    location VARCHAR(32) NOT NULL,
    start_date_time DATETIME NOT NULL,
    end_date_time DATETIME NOT NULL
);

CREATE TABLE CombatHero
(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    combat_id INT NOT NULL,
    hero_id INT,
    bot_id INT,
    team INT(1) NOT NULL,
    is_dead INT(1) DEFAULT 0,
    is_join INT(1) DEFAULT 0,
    is_out INT(1) DEFAULT 0,
    CONSTRAINT FK_combathero_combat FOREIGN KEY (combat_id)
        REFERENCES Combat (id) ON DELETE CASCADE ON UPDATE RESTRICT
);

CREATE TABLE CombatLog
(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    combat_id INT NOT NULL,
    is_bot_one INT(1) NOT NULL,
    is_bot_two INT(1) NOT NULL,
    hero_one_id INT,
    hero_two_id INT,
    bot_one_id INT,
    bot_two_id INT,
    hero_one_wstrike VARCHAR(16),
    hero_two_wstrike VARCHAR(16),
    hero_one_wblock VARCHAR(16),
    hero_two_wblock VARCHAR(16),
    hero_join INT(1) DEFAULT 0,
    hero_out INT(1) DEFAULT 0,
    hp_plus INT(6) DEFAULT 0,
    text TEXT NOT NULL,
    time TIME NOT NULL,
    CONSTRAINT FK_combatlog_combat FOREIGN KEY (combat_id)
        REFERENCES Combat (id) ON DELETE CASCADE ON UPDATE RESTRICT
);

CREATE TABLE Bot
(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(32) NOT NULL,
    level INT(3) NOT NULL,
    image_id INT NOT NULL,

    hp INT(6) NOT NULL,

    strenth INT(6) NOT NULL,
    dexterity INT(6) NOT NULL,
    intuition INT(6) NOT NULL,
    health INT(6) NOT NULL,

    swords INT(6) NOT NULL,
    axes INT(6) NOT NULL,
    knives INT(6) NOT NULL,
    clubs INT(6) NOT NULL,
    shields INT(6) NOT NULL,

    coordinate_x1 INT(6) NOT NULL,
    coordinate_y1 INT(6) NOT NULL,
    coordinate_x2 INT(6) NOT NULL,
    coordinate_y2 INT(6) NOT NULL
);

CREATE TABLE BotFeature
(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    bot_id INT NOT NULL,

    strenth VARCHAR(32),
    dexterity VARCHAR(32),
    intuition VARCHAR(32),
    health VARCHAR(32),

    swords VARCHAR(32),
    axes VARCHAR(32),
    knives VARCHAR(32),
    clubs VARCHAR(32),
    shields VARCHAR(32),

    protection_head VARCHAR(32),
    protection_breast VARCHAR(32),
    protection_zone VARCHAR(32),
    protection_leg VARCHAR(32),

    damage_min VARCHAR(32),
    damage_max VARCHAR(32),

    accuracy VARCHAR(32),
    dodge VARCHAR(32),
    devastate VARCHAR(32),
    durability VARCHAR(32),
    block_break VARCHAR(32),
    armor_break VARCHAR(32),

    hp VARCHAR(32),

    CONSTRAINT FK_botfeature_bot FOREIGN KEY (bot_id)
        REFERENCES Bot (id) ON DELETE CASCADE ON UPDATE RESTRICT
);

CREATE TABLE BotThing
(
    bot_id INT NOT NULL,
    thing_id INT NOT NULL,
    PRIMARY KEY (bot_id, thing_id),
    CONSTRAINT FK_bot FOREIGN KEY (bot_id)
        REFERENCES Bot (id) ON DELETE CASCADE ON UPDATE RESTRICT,
    CONSTRAINT FK_thing FOREIGN KEY (thing_id)
        REFERENCES Thing (id) ON DELETE CASCADE ON UPDATE RESTRICT
);

CREATE TABLE BotImage
(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    image VARCHAR(32) NOT NULL
);

CREATE TABLE Island
(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(32) NOT NULL,
    image VARCHAR(32) NOT NULL
);

CREATE TABLE IslandPart
(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    island_id INT NOT NULL,
    is_move INT(1) NOT NULL,
    coordinate_x INT(6) NOT NULL,
    coordinate_y INT(6) NOT NULL,
    
    CONSTRAINT FK_islandpart_island FOREIGN KEY (island_id)
        REFERENCES Island (id) ON DELETE CASCADE ON UPDATE RESTRICT
);

CREATE TABLE Building
(
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    parent_id INT,
    name VARCHAR(32) NOT NULL,
    plugin VARCHAR(32),
    coordinate_x1 INT(6),
    coordinate_y1 INT(6),
    coordinate_x2 INT(6),
    coordinate_y2 INT(6)
);

