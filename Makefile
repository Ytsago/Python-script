# -----------RULES-----------#
CC = c++
CFLAGS = -Wall -Wextra -Werror

# -----------PATHS-----------#
SRCDIR = src/
INCDIR = inc/
OBJDIR = .obj/

# -----------OTHER-----------#
OBJS = $(patsubst $(SRCDIR)%.cpp, $(OBJDIR)%.o, $(SRCS))

DEPS = $(OBJS:.o=.d)

HEADER = $(addprefix $(INCDIR), $(INC))

# LIBS = WIP

NAME = Pimpon

# -----------COMPILATION-----------#
all: $(NAME)
$(NAME): libs $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) $(LIBS) -o $(NAME)

$(OBJDIR)%.o: $(SRCDIR)%.cpp Makefile | $(OBJDIR)
	$(CC) $(CFLAGS) -I $(INCDIR) $(if $(LIBS),-I $(LIBDIR)$(INCDIR)) -c $< -o $@

$(OBJDIR): 
	mkdir -p $(OBJDIR) $(dir $(OBJS))

libs: 
	$(MAKE) -C $(LIBDIR) --no-print-directory


# -----------UTILS-----------#
clean: 
	rm -rf $(OBJDIR)
ifneq ($(LIBS),)
# WIP for libs

fclean: clean
	rm -f $(NAME)
# WIP for libs

re: fclean all

.PHONY: clean fclean, re, all

