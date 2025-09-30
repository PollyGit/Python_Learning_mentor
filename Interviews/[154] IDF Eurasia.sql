--1
--Даны 2 таблицы:
--список выданных кредитов:
--credit (credit_Id, sent_amount, date_requested, product_name)
--история платежей
--payments (credit_id, payment_date, payment_amount, npl_flag (флаг 1/0 платежа с просрочкой) )
--Вывести долю платежей за 2024 год, где изначальная сумма кредита (sent_amount) меньше 50 тыс и была просрочка.
--Запрос должен выдавать одно число: 0.3568

















