--1

--по данным из таблицы посчитать воронку из событий



with
flags as (
select user_id,
    bool_or(name = 'install') as has_install,  --bool_or(...) возвращает BOOLEAN  а не 0/1
    bool_or(name = 'onboarding') as has_onboarding,
    bool_or(name = 'register') as has_register,
    bool_or(name = 'setup') as has_setup
from events
where name in ('install','onboarding','register','setup')
group by user_id
)

select
    count(*) as cnt_users,
    count(*) filter (where has_install) as cnt_install,
    count(*) filter (where has_install  and has_onboarding) as cnt_onboarding,
    count(*) filter (where has_install and has_onboarding and has_register) as cnt_register,
    count(*) filter (where has_install
                        and has_onboarding
                        and has_register
                        and has_setup ) as cnt_setup
from flags;



--