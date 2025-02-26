--
-- PostgreSQL database dump for emm
--

-- Drop tables if they exist
DROP TABLE IF EXISTS "users_customuser_user_permissions";
DROP TABLE IF EXISTS "users_customuser_groups";
DROP TABLE IF EXISTS "users_customuser";
DROP TABLE IF EXISTS "institutes_institute";
DROP TABLE IF EXISTS "employees";
DROP TABLE IF EXISTS "django_session";
DROP TABLE IF EXISTS "django_migrations";
DROP TABLE IF EXISTS "django_content_type";
DROP TABLE IF EXISTS "django_admin_log";
DROP TABLE IF EXISTS "auth_permission";
DROP TABLE IF EXISTS "auth_group_permissions";
DROP TABLE IF EXISTS "auth_group";

--
-- Table structure for table "auth_group"
--
CREATE TABLE "auth_group" (
  "id" SERIAL PRIMARY KEY,
  "name" VARCHAR(150) NOT NULL UNIQUE
);

--
-- Table structure for table "auth_group_permissions"
--
CREATE TABLE "auth_group_permissions" (
  "id" BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  "group_id" INT NOT NULL,
  "permission_id" INT NOT NULL,
  CONSTRAINT "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" UNIQUE ("group_id", "permission_id"),
  CONSTRAINT "auth_group_permissions_group_id_b120cbf9_fk_auth_group_id" FOREIGN KEY ("group_id") REFERENCES "auth_group" ("id"),
  CONSTRAINT "auth_group_permissio_permission_id_84c5c92e_fk_auth_perm" FOREIGN KEY ("permission_id") REFERENCES "auth_permission" ("id")
);

--
-- Table structure for table "auth_permission"
--
CREATE TABLE "auth_permission" (
  "id" SERIAL PRIMARY KEY,
  "name" VARCHAR(255) NOT NULL,
  "content_type_id" INT NOT NULL,
  "codename" VARCHAR(100) NOT NULL,
  CONSTRAINT "auth_permission_content_type_id_codename_01ab375a_uniq" UNIQUE ("content_type_id", "codename"),
  CONSTRAINT "auth_permission_content_type_id_2f476e4b_fk_django_co" FOREIGN KEY ("content_type_id") REFERENCES "django_content_type" ("id")
);

-- Dumping data for table "auth_permission"
INSERT INTO "auth_permission" ("id", "name", "content_type_id", "codename") VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add employee', 6, 'add_employee'),
(22, 'Can change employee', 6, 'change_employee'),
(23, 'Can delete employee', 6, 'delete_employee'),
(24, 'Can view employee', 6, 'view_employee'),
(25, 'Can add institute', 7, 'add_institute'),
(26, 'Can change institute', 7, 'change_institute'),
(27, 'Can delete institute', 7, 'delete_institute'),
(28, 'Can view institute', 7, 'view_institute'),
(29, 'Can add user', 8, 'add_customuser'),
(30, 'Can change user', 8, 'change_customuser'),
(31, 'Can delete user', 8, 'delete_customuser'),
(32, 'Can view user', 8, 'view_customuser');

--
-- Table structure for table "django_admin_log"
--
CREATE TABLE "django_admin_log" (
  "id" SERIAL PRIMARY KEY,
  "action_time" TIMESTAMP(6) NOT NULL,
  "object_id" TEXT,
  "object_repr" VARCHAR(200) NOT NULL,
  "action_flag" SMALLINT NOT NULL CHECK ("action_flag" >= 0),
  "change_message" TEXT NOT NULL,
  "content_type_id" INT,
  "user_id" BIGINT NOT NULL,
  CONSTRAINT "django_admin_log_content_type_id_c4bce8eb_fk_django_co" FOREIGN KEY ("content_type_id") REFERENCES "django_content_type" ("id"),
  CONSTRAINT "django_admin_log_user_id_c564eba6_fk_users_customuser_id" FOREIGN KEY ("user_id") REFERENCES "users_customuser" ("id")
);

--
-- Table structure for table "django_content_type"
--
CREATE TABLE "django_content_type" (
  "id" SERIAL PRIMARY KEY,
  "app_label" VARCHAR(100) NOT NULL,
  "model" VARCHAR(100) NOT NULL,
  CONSTRAINT "django_content_type_app_label_model_76bd3d3b_uniq" UNIQUE ("app_label", "model")
);

-- Dumping data for table "django_content_type"
INSERT INTO "django_content_type" ("id", "app_label", "model") VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'permission'),
(3, 'auth', 'group'),
(4, 'contenttypes', 'contenttype'),
(5, 'sessions', 'session'),
(6, 'em_data', 'employee'),
(7, 'institutes', 'institute'),
(8, 'users', 'customuser');

--
-- Table structure for table "django_migrations"
--
CREATE TABLE "django_migrations" (
  "id" BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  "app" VARCHAR(255) NOT NULL,
  "name" VARCHAR(255) NOT NULL,
  "applied" TIMESTAMP(6) NOT NULL
);

-- Dumping data for table "django_migrations"
INSERT INTO "django_migrations" ("id", "app", "name", "applied") VALUES
(1, 'contenttypes', '0001_initial', '2025-02-20 21:40:31.957368'),
(2, 'contenttypes', '0002_remove_content_type_name', '2025-02-20 21:40:32.196088'),
(3, 'auth', '0001_initial', '2025-02-20 21:40:33.054072'),
(4, 'auth', '0002_alter_permission_name_max_length', '2025-02-20 21:40:33.164207'),
(5, 'auth', '0003_alter_user_email_max_length', '2025-02-20 21:40:33.178008'),
(6, 'auth', '0004_alter_user_username_opts', '2025-02-20 21:40:33.194060'),
(7, 'auth', '0005_alter_user_last_login_null', '2025-02-20 21:40:33.218736'),
(8, 'auth', '0006_require_contenttypes_0002', '2025-02-20 21:40:33.224638'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2025-02-20 21:40:33.248013'),
(10, 'auth', '0008_alter_user_username_max_length', '2025-02-20 21:40:33.270873'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2025-02-20 21:40:33.285404'),
(12, 'auth', '0010_alter_group_name_max_length', '2025-02-20 21:40:33.363014'),
(13, 'auth', '0011_update_proxy_permissions', '2025-02-20 21:40:33.372794'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2025-02-20 21:40:33.383541'),
(15, 'users', '0001_initial', '2025-02-20 21:40:33.936008'),
(16, 'admin', '0001_initial', '2025-02-20 21:40:34.115361'),
(17, 'admin', '0002_logentry_remove_auto_add', '2025-02-20 21:40:34.135261'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2025-02-20 21:40:34.157901'),
(19, 'institutes', '0001_initial', '2025-02-20 21:40:34.325415'),
(20, 'institutes', '0002_alter_institute_location_alter_institute_manager', '2025-02-20 21:40:34.484018'),
(21, 'institutes', '0003_remove_institute_manager_alter_institute_location_and_more', '2025-02-20 21:40:34.903528'),
(22, 'em_data', '0001_initial', '2025-02-20 21:40:35.166045'),
(23, 'em_data', '0002_remove_employee_user_alter_employee_institute_and_more', '2025-02-20 21:40:35.482666'),
(24, 'sessions', '0001_initial', '2025-02-20 21:40:35.581644'),
(25, 'users', '0002_remove_customuser_address_and_more', '2025-02-20 21:40:35.935602');

--
-- Table structure for table "django_session"
--
CREATE TABLE "django_session" (
  "session_key" VARCHAR(40) PRIMARY KEY,
  "session_data" TEXT NOT NULL,
  "expire_date" TIMESTAMP(6) NOT NULL
);
CREATE INDEX "django_session_expire_date_a5c62663" ON "django_session" ("expire_date");

-- Dumping data for table "django_session"
INSERT INTO "django_session" ("session_key", "session_data", "expire_date") VALUES
('u3a7pjg56iw2o4giy6b7em4g9cnqwjm9', '.eJxVjMEOwiAQRP-FsyGtZbvg0Xu_gcDuKlUDSWlPxn-XJj3oaZI3b-atfNjW5Lcqi59ZXRSo0y-LgZ6S94IfId-LppLXZY56V_TRVj0Vltf1cP8OUqiprbHrhagDIBessWOMBm9iXbTYIA8WCBmHwcAZkWjsHaIwCLRkpKg-X9QVN3Y:1tlX9b:Kmjrufw12jSNd9etfnCiLN9fTHmJhm0v-05cF0IIRHw', '2025-03-07 17:49:35.515820'),
('yaw4bc4s43ckl35z6adpgyan0zrnx308', '.eJxVjDsOwjAQBe_iGlnr-LuU9JzBWnsdHECOFCcV4u4QKQW0b2beS0Ta1hq3XpY4sTgLL06_W6L8KG0HfKd2m2We27pMSe6KPGiX15nL83K4fweVev3WYQAHTNag55CK0m4gy1ahQpO9CxisRgDtNfIYwJSCWavReEhIzjjx_gCwejZ0:1tmg4A:9Kbi4_Jygc9Jy4l8i-r0efrKHR2Hz02k4QY6l4sRF_o', '2025-03-10 21:32:42.771734');

--
-- Table structure for table "employees"
--
CREATE TABLE "employees" (
  "id" BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  "name" VARCHAR(255) NOT NULL,
  "rank" VARCHAR(255) DEFAULT NULL,
  "sort_number" INT DEFAULT NULL,
  "police_number" VARCHAR(255) DEFAULT NULL,
  "insurance_number" VARCHAR(255) DEFAULT NULL,
  "date_of_birth" DATE DEFAULT NULL,
  "date_of_appointment" DATE DEFAULT NULL,
  "created_at" TIMESTAMP(6) NOT NULL,
  "updated_at" TIMESTAMP(6) NOT NULL,
  "institute_id" BIGINT NOT NULL,
  CONSTRAINT "employees_institute_id_7ce3b6c9_fk_institutes_institute_id" FOREIGN KEY ("institute_id") REFERENCES "institutes_institute" ("id")
);

--
-- Table structure for table "institutes_institute"
--
CREATE TABLE "institutes_institute" (
  "id" BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  "name" VARCHAR(100) NOT NULL,
  "location" VARCHAR(255) NOT NULL
);

-- Dumping data for table "institutes_institute"
INSERT INTO "institutes_institute" ("id", "name", "location") VALUES
(7, 'معهد تأهيل الأفراد بالقاهرة', 'بالقاهرة');

--
-- Table structure for table "users_customuser"
--
CREATE TABLE "users_customuser" (
  "id" BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  "password" VARCHAR(128) NOT NULL,
  "last_login" TIMESTAMP(6) DEFAULT NULL,
  "is_superuser" BOOLEAN NOT NULL,
  "username" VARCHAR(150) NOT NULL UNIQUE,
  "first_name" VARCHAR(150) NOT NULL,
  "last_name" VARCHAR(150) NOT NULL,
  "email" VARCHAR(254) NOT NULL,
  "is_staff" BOOLEAN NOT NULL,
  "is_active" BOOLEAN NOT NULL,
  "date_joined" TIMESTAMP(6) NOT NULL,
  "institute_id" BIGINT DEFAULT NULL,
  CONSTRAINT "users_customuser_institute_id_5e17e3b6_fk_institute" FOREIGN KEY ("institute_id") REFERENCES "institutes_institute" ("id")
);

-- Dumping data for table "users_customuser"
INSERT INTO "users_customuser" ("id", "password", "last_login", "is_superuser", "username", "first_name", "last_name", "email", "is_staff", "is_active", "date_joined", "institute_id") VALUES
(7, 'pbkdf2_sha256$390000$klaTwAOmoF35J28408Ptsu$Szdh2agemQ4lwBY9Hnu/Wa5N/xNufKWa0gwKDP1G/lk=', '2025-02-24 21:32:42.721832', FALSE, 'soma', '', '', 'yasser.elbendary323@gmail.com', FALSE, TRUE, '2025-02-24 21:31:56.078430', 7);

--
-- Table structure for table "users_customuser_groups"
--
CREATE TABLE "users_customuser_groups" (
  "id" BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  "customuser_id" BIGINT NOT NULL,
  "group_id" INT NOT NULL,
  CONSTRAINT "users_customuser_groups_customuser_id_group_id_76b619e3_uniq" UNIQUE ("customuser_id", "group_id"),
  CONSTRAINT "users_customuser_gro_customuser_id_958147bf_fk_users_cus" FOREIGN KEY ("customuser_id") REFERENCES "users_customuser" ("id"),
  CONSTRAINT "users_customuser_groups_group_id_01390b14_fk_auth_group_id" FOREIGN KEY ("group_id") REFERENCES "auth_group" ("id")
);

--
-- Table structure for table "users_customuser_user_permissions"
--
CREATE TABLE "users_customuser_user_permissions" (
  "id" BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
  "customuser_id" BIGINT NOT NULL,
  "permission_id" INT NOT NULL,
  CONSTRAINT "users_customuser_user_pe_customuser_id_permission_7a7debf6_uniq" UNIQUE ("customuser_id", "permission_id"),
  CONSTRAINT "users_customuser_use_customuser_id_5771478b_fk_users_cus" FOREIGN KEY ("customuser_id") REFERENCES "users_customuser" ("id"),
  CONSTRAINT "users_customuser_use_permission_id_baaa2f74_fk_auth_perm" FOREIGN KEY ("permission_id") REFERENCES "auth_permission" ("id")
);

-- End of file