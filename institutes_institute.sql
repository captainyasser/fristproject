-- إدراج البيانات
INSERT INTO institutes_institute (id, name, location) VALUES
(7, 'معهد تأهيل الأفراد بالقاهرة', 'بالقاهرة')
ON CONFLICT (id) DO NOTHING;