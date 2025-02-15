from typeclasses.objects import Object


class Sittable(Object):

    def do_sit(self, sitter):
        """
        Called when trying to sit on/in this object.

        Args:
            sitter (Object): The one trying to sit down.

        """
        adjective = self.db.adjective or "on"
        msg_sitting_down = self.db.msg_sitting_down or f"You sit down {adjective} {self.key}."
        current = self.db.sitter
        if current:
            if current == sitter:
                sitter.msg(f"You are already sitting {adjective} {self.key}.")
            else:
                sitter.msg(
                    f"You can't sit {adjective} {self.key} "
                    f"- {current.key} is already sitting there!")
            return
        self.db.sitter = sitter
        sitter.db.is_sitting = self
        sitter.msg(msg_sitting_down)

    def do_stand(self, stander):
        """
        Called when trying to stand from this object.

        Args:
            stander (Object): The one trying to stand up.

        """
        current = self.db.sitter
        if not stander == current:
            stander.msg(f"You are not sitting {self.db.adjective} {self.key}.")
        else:
            self.db.sitter = None
            del stander.db.is_sitting
            stander.msg(f"You stand up from {self.key}.")
