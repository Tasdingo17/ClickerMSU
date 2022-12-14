"""Class for creating and placing options."""


import pygame as pg
import pygame_widgets
from .Button import Button
from collections import deque
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Option:
    """Base class for options."""

    font_name = "freesansbold.ttf"
    font_size = 32

    _COEF_SPACE_AFTER_NAME = 0.20

    def __init__(self, option_name: str, pos: tuple[int], name_pic: pg.Surface):
        """Create an object.

        :param option_name: name of the option
        :type option_name: str

        :param pos: position for start of option (bottomleft of name_pic)
        :type pos: tuple[int]

        :param name_pic: picture for pannel with option_name
        :type name_pic: pg.Surface

        :return: None
        """
        self.x_pos = pos[0]
        self.y_pos = pos[1]

        self.opt_name = option_name
        self.font = pg.font.Font(self.font_name, self.font_size)
        self.opt_name_text = self.font.render(self.opt_name, True, WHITE)
        self.name_pic = name_pic

    def change_font(self, font_name: str = None, font_size: int = None) -> None:
        """Change font and/or font_size for option's text.

        :param font_name: name of new font, if None - remains the same
        :type font_name: str

        :param font_size: new size, if None - remains the same
        :type font_size: int

        :return: None
        """
        if font_name:
            self.font_name = font_name
        if font_size:
            self.font_size = font_size
        self.font = pg.font.Font(self.font_name, self.font_size)
        return


class Option_switchable(Option):
    """Class for creating switchable option."""

    _COEF_SPACE_BETWEEN_SWITCH_AND_VAR = 0.07

    def __init__(self, option_name: str, pos: tuple[int], name_pic: pg.Surface,
                 current_var_pic: pg.Surface, switch_prev_pic: pg.Surface,
                 switch_next_pic: pg.Surface, variants: tuple[str] = None):
        """Create an object.

        :param option_name: name of the option
        :type option_name: str

        :param pos: position for start of option (bottomleft of name_pic)
        :type pos: tuple[int]

        :param name_pic: picture for pannel with option_name
        :type name_pic: pg.Surface

        :param current_var_pic: picture for pannel with current (selected) variant
        :type current_var_pic: pg.Surface

        :param switch_prev_pic: picture for button for switching to previous variant
        :type switch_prev_pic: pg.Surface

        :param switch_next_pic: picture for button for switching to next variant
        :type switch_next_pic: pg.Surface

        :param variants: possible values
        :type variants: tuple[str]

        :return: None
        """
        super().__init__(option_name, pos, name_pic)
        self.switch_prev_pic = switch_prev_pic
        self.curr_var_pic = current_var_pic
        self.switch_next_pic = switch_next_pic

        self.variants = deque(variants) if variants else None
        self.curr_var = self.variants[0] if variants else None
        self.curr_var_text = self.font.render(self.curr_var, True, WHITE)

        self._make_gui()

    def _make_gui(self) -> None:
        """Make gui for options.

        :return: None
        """
        self.rect_name_pic = self.name_pic.get_rect(bottomleft=(self.x_pos, self.y_pos))
        self.rect_opt_name_text = self.opt_name_text.get_rect(center=self.rect_name_pic.center)

        # Space between opt name panel and switch previous button
        shift1 = self.rect_name_pic.width * self._COEF_SPACE_AFTER_NAME
        # Space between switch buttons and current variant
        shift2 = self.rect_name_pic.width * self._COEF_SPACE_BETWEEN_SWITCH_AND_VAR

        switch_prev_pos = (self.rect_name_pic.right + shift1, self.y_pos)
        # self.rect_switch_prev = self.switch_prev.get_rect(bottomleft=switch_prev_pos)
        self.switch_prev_button = Button(self.switch_prev_pic, switch_prev_pos, "")
        self.switch_prev_button.set_pos(bottomleft=switch_prev_pos)

        curr_var_pos = (self.switch_prev_button.get_rect().right + shift2, self.y_pos)
        self.rect_curr_var_pic = self.curr_var_pic.get_rect(bottomleft=curr_var_pos)
        self.rect_curr_var_text = self.curr_var_text.get_rect(center=self.rect_curr_var_pic.center)

        switch_next_pos = (self.rect_curr_var_pic.right + shift2, self.y_pos)
        self.switch_next_button = Button(self.switch_next_pic, switch_next_pos, "")
        self.switch_next_button.set_pos(bottomleft=switch_next_pos)

        return

    def update(self, screen: pg.Surface) -> None:
        """Update options images on screen.

        :param screen: screen where to show
        :type screen: pg.Surface

        :return: None
        """
        screen.blit(self.name_pic, self.rect_name_pic)
        screen.blit(self.opt_name_text, self.rect_opt_name_text)

        self.switch_prev_button.update(screen)
        self.switch_next_button.update(screen)

        screen.blit(self.curr_var_pic, self.rect_curr_var_pic)
        screen.blit(self.curr_var_text, self.rect_curr_var_text)

    def check_for_switch_prev(self, position: tuple[int]) -> bool:
        """Check if possition corresponds to switch prev button.

        :param position: sposition of options' click
        :type position: tuple[int]

        :return: bool
        """
        return self.switch_prev_button.checkForInput(position)

    def check_for_switch_next(self, position: tuple[int]) -> bool:
        """Check if possition corresponds to switch next button.

        :param position: sposition of options' click
        :type position: tuple[int]

        :return: bool
        """
        return self.switch_next_button.checkForInput(position)

    def switch_next(self) -> None:
        """Switch current variant to next.

        :return: bool
        """
        self.variants.rotate(-1)
        self.curr_var = self.variants[0]
        self.curr_var_text = self.font.render(self.curr_var, True, WHITE)

    def switch_prev(self) -> None:
        """Switch current variant to previous.

        :return: bool
        """
        self.variants.rotate(1)
        self.curr_var = self.variants[0]
        self.curr_var_text = self.font.render(self.curr_var, True, WHITE)

    def switch_mb(self, position: tuple[int]) -> bool:
        """Check if position corresponds to switch buttons and if it is then switch.

        :param position: sposition of options' click to check
        :type position: tuple[int]

        :return: bool
        """
        if self.check_for_switch_prev(position):
            self.switch_prev()
            return True
        if self.check_for_switch_next(position):
            self.switch_next()
            return True
        return False

    def set_curr_value(self, value: str) -> None:
        """Set current value for option.

        :param value: value ti set
        :type value: str

        :return: bool
        """
        if value not in self.variants:
            raise ValueError(f"Wrong value for option: {self.opt_name}")
        while value != self.variants[0]:
            self.variants.rotate(-1)
        self.curr_var = self.variants[0]
        self.curr_var_text = self.font.render(self.curr_var, True, WHITE)
        return


class Option_slider(Option):
    """Class for creating option with slider."""

    _COEF_SLIDER_WIDTH = 1.5
    _COEF_SLIDER_HEIGHT = 0.3
    _COEF_OUTPUT_SIZE = 0.5
    _COEF_SPACE_SLIDER_OUTPUT = 0.1

    def __init__(self, display: pg.Surface, option_name: str, pos: tuple[int], name_pic: pg.Surface,
                 left: int = 0, right: int = 100, step: int = 1, **kwargs):
        """Create an object.

        :param display: Surface to draw on
        :type display: pg.Surface

        :param option_name: name of the option
        :type valoption_nameue: str

        :param pos: position for start of option (bottomleft of name_pic)
        :type pos: tuple[int]

        :param name_pic: picture for pannel with option_name
        :type name_pic: pg.Surface

        :param left: slider's left bound
        :type left: int

        :param right: slider's right bound
        :type right: int

        :param step: slider's step
        :type step: int

        :return: None
        """
        super().__init__(option_name, pos, name_pic)
        self._make_gui(display, left, right, step, **kwargs)

    def _create_slider(self, display: pg.Surface, left: int = 0, right: int = 100,
                       step: int = 1, **kwargs) -> Slider:
        """Create slider.

        :param display: Surface to draw on
        :type display: pg.Surface

        :param left: slider's left bound
        :type left: int

        :param right: slider's right bound
        :type right: int

        :param step: slider's step
        :type step: int

        :return: Slider
        """
        # Space between opt name panel and slider
        shift1 = self.rect_name_pic.width * self._COEF_SPACE_AFTER_NAME

        # Set slider
        slider_width = int(self.rect_name_pic.width * self._COEF_SLIDER_WIDTH)
        slider_height = int(self.rect_name_pic.height * self._COEF_SLIDER_HEIGHT)
        slider_pos = (self.rect_name_pic.topright[0] + shift1,
                      self.rect_name_pic.centery - slider_height // 2)
        self.slider = Slider(display, slider_pos[0], slider_pos[1],
                             slider_width, slider_height,
                             min=left, max=right, step=step, **kwargs)
        if "slider_colour" in kwargs:
            self.slider.colour = kwargs["slider_colour"]
        if "handle_colour" in kwargs:
            self.slider.handleColour = kwargs["handle_colour"]
        if "initial_value" in kwargs:
            self.slider.value = kwargs["initial_value"]
        return self.slider

    def _create_output(self, display: pg.Surface, **kwargs) -> TextBox:
        """Create output for slider.

        :param display: Surface to draw on
        :type display: pg.Surface

        :return: TextBox
        """
        # Set output (square under the center of slider)
        output_size = self.rect_name_pic.height * self._COEF_OUTPUT_SIZE
        output_pos = (self.slider.getX() + self.slider.getWidth()
                      + self.rect_name_pic.width * self._COEF_SPACE_SLIDER_OUTPUT,
                      self.rect_name_pic.centery - output_size // 2)
        self.output = TextBox(display, output_pos[0], output_pos[1],
                              output_size, output_size, fontSize=self.font_size, **kwargs)
        self.output.disable()  # Act as label instead of textbox
        return self.output

    def _make_gui(self, display: pg.Surface, left: int = 0, right: int = 100,
                  step: int = 1, **kwargs) -> None:
        """Make gui for options.

        :param display: Surface to draw on
        :type display: pg.Surface

        :param left: slider's left bound
        :type left: int

        :param right: slider's right bound
        :type right: int

        :param step: slider's step
        :type step: int

        :return: None
        """
        self.rect_name_pic = self.name_pic.get_rect(bottomleft=(self.x_pos, self.y_pos))
        self.rect_opt_name_text = self.opt_name_text.get_rect(center=self.rect_name_pic.center)

        self._create_slider(display, left, right, step, **kwargs)
        self._create_output(display, **kwargs)
        return

    def update(self, screen: pg.Surface) -> None:
        """Update options images on screen.

        :param screen: screen to draw on
        :type screen: pg.Surface

        :return: None
        """
        screen.blit(self.name_pic, self.rect_name_pic)
        screen.blit(self.opt_name_text, self.rect_opt_name_text)
        self.output.draw()
        self.slider.draw()

    def get_value(self) -> int:
        """Get slider's value.

        :return: int
        """
        return self.slider.getValue()

    def set_value(self, val: int) -> None:
        """Set value for slider.

        :param val: value of the slider to set
        :type val: int

        :return: None
        """
        self.slider.value = val
        return

    def update_slider(self, events: list[pg.event.Event]) -> None:
        """Update slider.

        :param events: events in option (any)
        :type events: list[pg.event.Event]

        :return: None
        """
        self.output.setText(self.slider.getValue())
        pygame_widgets.update(events)
        return
