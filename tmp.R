require(tidyverse)
d %>% 
  group_by(target) %>% 
  summarise(condition = first(target_type),
            character = first(target),
            frequency = first(target_frequency)) %>% 
  ungroup() %>% 
  group_by(condition) %>% 
  arrange(condition) %>% 
  nrow()
  write_csv('~/Desktop/characters.csv')


d %>% 
  group_by(subnum) %>% 
  summarise(age = round(first(age)/12, digits=2),
            gender = first(gender)) %>% 
  arrange(-desc(subnum)) %>% 
  write_csv('~/Desktop/participants.csv')


d %>% 
  #group_by(target_type) %>% 
  filter(subnum == 1) %>% 
  group_by(block, radical) %>% 
  arrange(desc(trial)) %>% 
  select(target, radical, target_type, block, trial) %>%
  write_csv('~/Desktop/blocks.csv')
