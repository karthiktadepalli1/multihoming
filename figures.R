# Purpose: creating figures for the multihoming paper.

#---------------SETUP-----------------------

# installing required packages if you don't have them, loading them if you do
if (!require("pacman")) install.packages("pacman")
pacman::p_load(tidyverse, gridExtra, grid, latex2exp, wesanderson)

# set figures to output in overleaf directly - modify the path to wherever you want
fig_path <- "~/Dropbox/Apps/Overleaf/Uber Project/simulations/"
save <- function(plot, name, ...) {
  ggsave(paste0(fig_path, name), plot, ...)
}

# visual/color settings for the figures
theme_set(theme_minimal() + theme(
  axis.title = element_text(size = 17),
  axis.text = element_text(size=14),
  strip.text = element_text(size = 15),
  plot.title = element_text(hjust=0.5, size = 19),
  legend.title = element_blank()))

palette <- wes_palette("Darjeeling1", n=2, "discrete")

#----------------FIGURE 1-----------------

# read in data, select only the range where pi_2 is nonnegative
br <- read_csv("single.csv") %>%
  bind_rows(read_csv("multi.csv")) %>%
  filter(alpha >= 0.93) %>%
  mutate(type = ifelse(type == "multi", "multihoming", "singlehoming"))

# make price/latency variables
br <- br %>%
  mutate(w_1 = alpha * s_1 * (s_1 + s_2)/d_1,
         w_2 = alpha * s_2 * (s_1 + s_2)/d_1,
         l_1 = ifelse(type == "singlehoming",
                      alpha * d_1/s_1,
                      (alpha * d_1 + d_2)/(s_1+s_2)),
         l_2 = ifelse(type == "singlehoming",
                      d_2/s_2,
                      (alpha * d_1 + d_2)/(s_1+s_2)),
         p_1 = 1 - d_1 - d_2 - l_1,
         p_2 = 1 - d_1 - d_2 - l_2)

# figure 1 - profit decreases as alpha decreases under multihoming
p <- ggplot(br, aes(x = alpha, y = pi_1, color = type, linetype = type)) + 
  geom_line() + 
  scale_color_manual(values = palette) + 
  labs(x = TeX("Efficient firm's cost factor ($\\alpha$)"), y = "Efficient firm's profit")
p
save(p, "profit1.png", width = 7, height = 4.4)

#---------------FIGURE 2--------------------

# general plotting function for any given variable with alpha for both firms
# used for figures 2-6
plot_a <- function(var, lab, both = T) {
  v1 <- paste0(var, "_1")
  v2 <- paste0(var, "_2")
  br %>% pivot_longer(cols = c(v1, v2), values_drop_na = T) %>%
    mutate(name = paste(
      ifelse(name == v1, "Efficient firm's", "Inefficient firm's"), lab)) %>%
    ggplot(aes(x = alpha, y = value, color = type, linetype = type)) +
    facet_wrap(~name, scales = "free") + 
    geom_line() + 
    scale_color_manual(values = palette) +
    labs(x = TeX("Efficient firm's cost factor ($\\alpha$)"), y = "")
}

# figure 2
p <- plot_a("w", "wage") +
  scale_y_continuous(limits = c(0.14, 0.31), breaks = seq(0.15, 0.3, 0.05))
p
save(p, "wages.png", width = 11, height = 4.4)

#----------------FIGURE 3----------------

p <- plot_a("d", "demand") +
  scale_y_continuous(limits = c(0.027, 0.041))
p
save(p, "demand.png", width = 11, height = 4.4)

#----------------FIGURE 4-----------------

p <- plot_a("p", "price") +
  ylim(0.3, 0.5)
p 
save(p, "prices.png", width = 11, height = 4.4)

#----------------FIGURE 5-----------------

p <- plot_a("s", "supply")
p
save(p, "supply.png", width = 11, height = 4.4)

#----------------FIGURE 6-----------------

p <- plot_a("l", "rider latency") +
  scale_y_continuous(limits = c(0.44, 0.6))
p
save(p, "latency.png", width = 11, height = 4.4)

#----------------FIGURE 7-----------------

# read in data again
full <- read_csv("multi.csv") %>%
  bind_rows(read_csv("single.csv")) %>%
  mutate(type = ifelse(type == "multi", "multihoming", "singlehoming"))

# identify shutdown threshold a* for singlehoming and multihoming
thresholds <- full %>% filter(pi_2 < 0) %>%
  group_by(type) %>%
  select(alpha) %>%
  summarise_all(max)
thresholds[[1,2]] # multihoming threshold is 0.9257
thresholds[[2,2]] # singlehoming threshold is 0.6104

# figure 7
p <- full %>%
  filter(pi_2 > 0) %>%
  ggplot(aes(x = alpha, y = pi_2, color = type, linetype = type)) +
  geom_line() +
  scale_color_manual(values = palette) +
  geom_hline(yintercept = 0) +
  geom_text(aes(0.8, 0.0002, label = "Inefficient firm's shutdown point"), 
            size=4, color = 'black') +
  labs(x = TeX("Efficient firm's cost factor ($\\alpha$)"),
       y = "Inefficient firm's profit")
p
save(p, "shutdown.png", width = 7, height = 4.4)

