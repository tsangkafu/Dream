from nodes import Node
from settings import *

class EventManager():
    def __init__(self, level):
        self.level = level
        self.dialog = self.level.dialog
        self.battle = self.level.battle
        self.node_replaced = False
        self.bonfire_checked = False
        # to indicate if the equipment ui is popped after reaching bonfire
        self.equipment_popped = False
        self.NPC_dialog_started = False
        self.NPC_fight_started = False
        self.selected_NPC = None
        self.selected_fight_NPC = None

    def handling(self):
        # a method to pass in the dialog that trigger the fight (the dialog right before the fight)
        # since start_dialog and the end_dialog(after fight dialog) is a pair
        # the index right after the trigger_dialog indicate that the fight has end
        def NPC_fight_handle(trigger_dialog):
            # if the end dialog is already triggered, fight ends
            # this is to prevent the selected_fight_NPC to be set to None
            if trigger_dialog + 1 in self.dialog.finished_scenes: return

            if trigger_dialog in self.dialog.finished_scenes:
                self.NPC_fight_started = True
                self.selected_fight_NPC = self.selected_NPC
        
        # all scene in medieval
        if self.level.theme == "md":
            """
            Unlocking hidden scenes here.
            """
            # after talking to Prudentius, unlock more Ursinus dialogs
            if 300 in self.dialog.finished_scenes:
                self.dialog.unlock_scene([500])
            # unlock Ursina cliff encounter only after defiant hunter is killed and after talking with Prudentius
            if 18 in self.dialog.finished_scenes and 500 in self.dialog.finished_scenes:
                self.dialog.unlock_scene([501])
            # after talking to Ursinus, unlock more Egnatius dialogs
            if 501 in self.dialog.finished_scenes:
                self.dialog.unlock_scene([503])
            # after killing Ursinus, unlock more Egnatius and Maire dialogs
            if 405 in self.dialog.finished_scenes:
                # 508 is the Maire threatening dialog
                # after getting dismal head, the fight with Maire can start right away
                # and 508 is not important anymore
                list_to_unlock = [505, 508] if not "Dismal Head" in self.level.player.items else [505]
                # if Maire is killed before, don't unlock her threatening scene
                self.dialog.unlock_scene(list_to_unlock)
            # after talking to Maire, unlock more Egnatius dialogs
            if 508 in self.dialog.finished_scenes:
                self.dialog.unlock_scene([504])
            # after killing Maire, unlock more Egnatius dialogs
            if 403 in self.dialog.finished_scenes:
                self.dialog.unlock_scene([506])
            # after killing Maire and talking with Engatius, unlock Prudentius dialogs
            if 506 in self.dialog.finished_scenes:
                # also remove previous Predentius scene
                self.dialog.unlock_scene([507], [301])
            # after talking with Prudentius unlock more Iduma dialog
            if 507 in self.dialog.finished_scenes:
                self.dialog.unlock_scene([509])

            # Maire fight requires Dismal Head
            if "Dismal Head" in self.level.player.items:
                # if you have talked with Egnatius about Maire, unlock the fight
                if 504 in self.dialog.finished_scenes:
                    self.dialog.unlock_scene([402, 403])
                # if you acquire dismal head before talking with Egnatius
                # skip over (remove) the first 2 dialogs with Maire
                else:
                    self.dialog.unlock_scene([402, 403], [302, 303])

                if 403 in self.dialog.finished_scenes:
                    self.player.items.remove("Dismal Head")

            # revenge to Ursinus after bonehand is killed
            if 14.5 in self.dialog.finished_scenes or 502.5 in self.dialog.finished_scenes:
                # this also removes previous Egnatius dialog if not finished
                self.dialog.unlock_scene([404, 405], [304, 503])
            # after Iduma asked Lucas to submit himself, unlock Egnatius fight
            if 509 in self.dialog.finished_scenes:
                self.dialog.unlock_scene([406, 407])
            # after killing Egnatius, unlock Prudentius battle
            if 407 in self.dialog.finished_scenes:
                self.dialog.unlock_scene([408, 409])
            # Iduma boss fight dialog
            if 409 in self.dialog.finished_scenes:
                self.dialog.unlock_scene([400, 401], [305])

            """
            Handle scenes related to collision
            """
            for node in self.level.node_sprites:
                # opening scene
                if node.ab_pos == (7, 15):
                    self.encounter(node, 0, 0, -1)
                # stone mumbler
                if node.ab_pos == (7, 13):
                    self.encounter(node, 1, 2, 0)
                # bonfire 1
                if node.ab_pos == (4, 12):
                    self.encounter(node, 8, 9, 3)
                # bonfire 2
                if node.ab_pos == (3, 5):
                    self.encounter(node, 10, 10, -1)
                # taintpaw
                if node.ab_pos == (3, 14):
                    self.encounter(node, 4, 5, 1)
                # corpsesword boss fight
                if node.ab_pos == (6, 11):
                    self.encounter(node, 6, 7, 2)
                # bowel skinner
                if node.ab_pos == (2, 10):
                    self.encounter(node, 3, 3, -1)
                # phantomfreak boss fight
                if node.ab_pos == (1, 15):
                    if 12 not in self.dialog.finished_scenes and 12.5 not in self.dialog.finished_scenes:
                        if 502 in self.dialog.finished_scenes:
                            self.encounter(node, 11.5, 12.5, 4)
                        else:
                            self.encounter(node, 11, 12, 4)
                # bondhand
                if node.ab_pos == (0, 11):
                    if 502 in self.dialog.finished_scenes:
                        if 14 in self.dialog.finished_scenes and self.level.player.rect.colliderect(node.rect):
                            self.dialog.unlock_scene([502.5])
                            self.dialog.start_dialog(502.5)
                            return
                        self.encounter(node, 13.5, 14.5, 5)
                    else:
                        self.encounter(node, 13, 14, 5)
                # dreadsnare
                if node.ab_pos == (4, 9):
                    self.encounter(node, 15, 16, 6)
                # defiant hunter & special encounter with Ursinus
                if node.ab_pos == (1, 8):
                    self.encounter(node, 17, 18, 7)
                    if 501 in self.dialog.finished_scenes and self.level.player.rect.colliderect(node.rect):
                        self.dialog.unlock_scene([502])
                        self.dialog.start_dialog(502)
                    if 502 in self.dialog.finished_scenes \
                    and 14.5 not in self.dialog.finished_scenes \
                    and 502.5 not in self.dialog.finished_scenes:
                        # play the falling sound after the player is kicked off the cliff
                        if self.level.player.rect.colliderect(node.rect) and not self.level.sfx.plot_channel.get_busy():
                            self.level.sfx.plot_channel.play(self.level.sfx.falling)
                        for target_node in self.level.node_sprites:
                            # find the node where the mouse is clicked
                            if target_node.ab_pos == (0, 11):
                                self.level.player.set_target(target_node.rect.topleft)
                                # disable the walking sound
                                self.level.player.walking = False
                # flamepod
                if node.ab_pos == (5, 7):
                    self.encounter(node, 19, 20, 8)
                # grimescream
                if node.ab_pos == (6, 3):
                    self.encounter(node, 21, 22, 9)
                # cindersword
                if node.ab_pos == (8, 4):
                    self.encounter(node, 23, 24, 10)
                # bladetalon
                if node.ab_pos == (5, 1):
                    self.encounter(node, 25, 26, 11)
                # behemoth boss fight
                if node.ab_pos == (3, 0):
                    self.encounter(node, 27, 28, 12)
                # mournfoot
                if node.ab_pos == (2, 2):
                    self.encounter(node, 29, 30, 13)
                # dismal abortion
                if node.ab_pos == (1, 4):
                    if not 32 in self.dialog.finished_scenes and not 32.5 in self.dialog.finished_scenes:
                        if 504 in self.dialog.finished_scenes:
                            self.encounter(node, 31.5, 32.5, 14)
                        else:
                            self.encounter(node, 31, 32, 14)
                # village
                if node.ab_pos == (8, 9):
                    if self.level.player.rect.collidepoint(node.rect.center):
                        # if the player just left the village, do not show the village
                        if not self.level.player.exiting:
                            self.level.in_village = True

            # dialog in village
            # when equipment is shown, don't trigger the following actions
            if self.level.in_village and not self.level.equipment.show:
                """
                NPC fight configuration.
                """
                if self.NPC_fight_started and self.selected_fight_NPC != None:
                    if self.selected_fight_NPC.name == "Iduma Macer":
                        self.encounter(node, 400, 401, 19)
                    elif self.selected_fight_NPC.name == "Maire Whelani":
                        self.encounter(node, 402, 403, 15)
                    elif self.selected_fight_NPC.name == "Ursinus Clodianus":
                        self.encounter(node, 404, 405, 16)
                    elif self.selected_fight_NPC.name == "Egnatius Barbatus":
                        self.encounter(node, 406, 407, 18)
                    elif self.selected_fight_NPC.name == "Prudentius Stolo":
                        self.encounter(node, 408, 409, 17)
                
                if self.selected_NPC == None:
                    # select which npc is being talked to
                    for npc in self.level.npc_sprites:
                        if npc.v_rect.collidepoint(pygame.mouse.get_pos()):
                            for event in pygame.event.get():
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    self.NPC_dialog_started = True
                                    # get the NPC who is clicked only if the npc has dialog
                                    if npc.dialog_count < len(npc.dialogs):
                                        self.selected_NPC = npc

                # if self.selected_NPC != None
                else:
                    if self.selected_NPC.dialog_count < len(self.selected_NPC.dialogs) and self.NPC_dialog_started:
                        # some dialog may not be triggered by clicking the NPC
                        # therefore, the following line will recalculate the dialog count pointer where the NPC should be at
                        # so that when talking to the NPC he/she will always start at the correct index
                        # otherwise, it may requires a few more clicks (incrementing dialog count) to get there
                        for i in range(self.selected_NPC.dialog_count, len(self.selected_NPC.dialogs)):
                            if self.selected_NPC.dialogs[i] in self.dialog.finished_scenes \
                            and self.selected_NPC.dialog_count < len(self.selected_NPC.dialogs) - 1:
                                self.selected_NPC.dialog_count += 1

                        if self.selected_NPC.dialog_count < len(self.selected_NPC.dialogs):
                            self.dialog.start_dialog(self.selected_NPC.dialogs[self.selected_NPC.dialog_count])
                            
                        # go to the next scene if finished
                        if self.selected_NPC.dialogs[self.selected_NPC.dialog_count] in self.dialog.finished_scenes:
                            self.dialog_started = False
                            self.selected_NPC.dialog_count += 1

                            """
                            Trigger the npc fight right after the selected dialog ends.
                            Scene number put here should be the starting dialog that triggers the fight.
                            Other conditions can be set as well.
                            """
                            NPC_fight_handle(400)
                            NPC_fight_handle(402)
                            NPC_fight_handle(404)
                            NPC_fight_handle(406)
                            NPC_fight_handle(408)

                            # clean the selected_NPC so that the player can talk to other NPC
                            self.selected_NPC = None

        elif self.level.theme == "gs":
            for node in self.level.node_sprites:
                # opening scene
                if node.ab_pos == (1, 15):
                    self.encounter(node, 50, 50, -1)
                # maddog
                if node.ab_pos == (2, 13):
                    self.encounter(node, 51, 52, 20)
                # pietro ferocious
                if node.ab_pos == (0, 11):
                    self.encounter(node, 53, 54, 21)
                # frankie blades
                if node.ab_pos == (3, 10):
                    self.encounter(node, 55, 56, 22)
                # davide coldblooded
                if node.ab_pos == (5, 12):
                    self.encounter(node, 57, 58, 23)
                # angelo the animal
                if node.ab_pos == (6, 9):
                    self.encounter(node, 59, 60, 24)
                # carlo hammer
                if node.ab_pos == (4, 8):
                    self.encounter(node, 61, 62, 25)
                # johnny hands boss fight
                if node.ab_pos == (6, 6):
                    self.encounter(node, 63, 64, 26)
                # vito savage
                if node.ab_pos == (5, 4):
                    self.encounter(node, 65, 66, 27)
                # antonio viper
                if node.ab_pos == (2, 5):
                    self.encounter(node, 67, 68, 28)
                # incendiary giovanni
                if node.ab_pos == (1, 3):
                    self.encounter(node, 69, 70, 29)
                # salvatore scarface
                if node.ab_pos == (3, 1):
                    self.encounter(node, 71, 72, 30)
                # francesco pistolero
                if node.ab_pos == (7, 2):
                    self.encounter(node, 73, 74, 31)
                

        elif self.level.theme == "cp":
            pass

    def encounter(self, node, before_dialog, after_dialog, scene):
        def replace_node():
            # change the node type to a fade
            node.node_type = node.node_type + "_faded"
            # update the image to a faded node
            node.image = node.get_image(node.node_type)
            self.node_replaced = True
            # after replacing the node, means the fight has ended, time to update item
            self.level.equipment.update_item = True
        
        # decide if it is a special NPC fight scene
        if self.level.theme == "md":
            self.special = True if scene >= 15 else False
        elif self.level.theme == "gs":
            self.special = True if scene >= 32 else False

        # if it is a special NPC fight
        if self.special:
            self.dialog.start_dialog(before_dialog)
            if self.dialog.dialog_end and scene not in self.level.battle.finished_battle:
                # start the battle
                self.battle.start(self.level.enemy_sprites.sprites()[scene], scene)
                self.dialog.end_battle_dialog_end = False
                # turn the village interface off, this may affect the cursor if turned on
                self.level.in_village = False

            if scene in self.level.battle.finished_battle:
                # if the player is dead
                if self.level.player.hp <= 0:
                    self.level.status = 0

                else:
                    # kill the NPC on the screen after the battle ends
                    if self.selected_fight_NPC != None:
                        NPC_name = self.selected_fight_NPC.name
                        for npc in self.level.npc_sprites:
                            if npc.name == NPC_name:
                                npc.kill()
                                # after the fight ends, means the fight has ended, time to update item
                                self.level.equipment.update_item = True

                    # when the end battle dialog has not finished
                    if not self.dialog.end_battle_dialog_end:
                        # start the end battle dialog, where "end_battle_dialog_end" will be triggered at the end
                        self.dialog.start_end_battle_dialog(ENEMIES[scene])
                        # after the dialog ends
                        if self.dialog.end_battle_dialog_end:
                            if self.battle.upgrading:
                                # activiate the upgrade dialog
                                self.dialog.upgrade_dialog_end = False
                    # when the end battle dialog is finished and there is a upgrade
                    elif not self.dialog.upgrade_dialog_end:
                        self.dialog.start_upgrade_dialog(self.level.player)
                        # when the "after dialog" finishes, deactivate the upgrading to prevent upgrade dialog
                        if self.dialog.upgrade_dialog_end:
                            self.battle.upgrading = False
                    
                    # "upgrade_dialog_end" is false
                    elif self.dialog.upgrade_dialog_end:
                        self.dialog.start_dialog(after_dialog)
                        if after_dialog in self.dialog.finished_scenes:
                            # disable self.NPC_fight_started anyway
                            self.selected_fight_NPC = None
                            self.level.in_village = True
                            # end the NPC fight
                            self.NPC_fight_started = False

        # if it is not a special NPC fight
        elif self.level.player.rect.collidepoint(node.rect.center):
            # when the player move to other node other than the village, disable exiting
            # meaning that the player already exit, village can be shown again when re-enter
            if self.level.theme == "md":
                if node.ab_pos != (8, 9): self.level.player.exiting = False
            elif self.level.theme == "gs":
                if node.ab_pos != (8, 13): self.level.player.exiting = False

            self.dialog.start_dialog(before_dialog)

            # if scene number > 0, there is a fight
            if scene >= 0:
                # when fight first starts
                if self.dialog.dialog_end and scene not in self.level.battle.finished_battle:
                    self.node_replaced = False
                    # find the cooresponding enemy index
                    # enemies in different theme are in a same dict
                    # therefore offset for each theme is needed
                    index = scene
                    for enemy in self.level.enemy_sprites.sprites():
                        if enemy.theme == "gs":
                            index = scene - 20
                    self.battle.start(self.level.enemy_sprites.sprites()[index], scene)
                    self.dialog.end_battle_dialog_end = False
                # after finishing the battle
                if scene in self.level.battle.finished_battle:
                    self.level.battle_sfx_start = False
                    # change the status to gameover if the player is dead
                    if self.level.player.hp <= 0:
                        self.level.status = 0
                    else:
                        # when the end battle dialog has not finished
                        if not self.dialog.end_battle_dialog_end:
                            # start the end battle dialog, where "end_battle_dialog_end" will be triggered at the end
                            self.dialog.start_end_battle_dialog(ENEMIES[scene])
                            # after the dialog ends
                            if self.dialog.end_battle_dialog_end:
                                if self.battle.upgrading:
                                    # activiate the upgrade dialog
                                    self.dialog.upgrade_dialog_end = False
                        # when the end battle dialog is finished and there is a upgrade
                        elif not self.dialog.upgrade_dialog_end:
                            # when the "after dialog" finishes, dialog.upgrade_dialog_end will be set to true
                            self.dialog.start_upgrade_dialog(self.level.player)
                            # deactivate the upgrading to prevent upgrade dialog
                            if self.dialog.upgrade_dialog_end:
                                self.battle.upgrading = False

                        # "upgrade_dialog_end" is false anyway
                        elif self.dialog.upgrade_dialog_end:
                            self.dialog.start_dialog(after_dialog)

                        if not self.node_replaced:
                            replace_node()

            # if it is not a fight scene
            else:
                # if it is bonfire
                if node.node_type == "bonfire":
                    self.equipment_popped = False
                    if not self.bonfire_checked:
                        self.level.player.hp = self.level.player.max_hp
                        self.node_replaced = False
                    if not self.node_replaced:
                        self.bonfire_checked = True
                        replace_node()
                # if the bonfire has faded out
                elif node.node_type == "bonfire_faded":
                    # pop out the equipment ui when the dialog is finished
                    if before_dialog in self.dialog.finished_scenes:
                        if not self.equipment_popped:
                            self.level.equipment.show = True
                            self.equipment_popped = True
                            self.bonfire_checked = False