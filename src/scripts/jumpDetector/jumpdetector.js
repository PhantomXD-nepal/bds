import { system, world } from "@minecraft/server";
export class onJumpAfterEvent {
  constructor(callback, tickDelay) {
    let tick = 0;
    if (tickDelay) tick = tickDelay;
    system.runInterval(() => {
      for (const player of world.getAllPlayers()) {
        if (player.hasTag(onJumpAfterEvent.jumpTag)) {
          if (player.isOnGround) player.removeTag(onJumpAfterEvent.jumpTag);
        } else if (player.isJumping) {
          player.addTag(onJumpAfterEvent.jumpTag);
          callback({
            player: player,
            location: player.location,
            dimension: player.dimension,
          });
        }
      }
    }, tick);
  }
}
onJumpAfterEvent.jumpTag = "afterevent.jumped";

//Usage

// import { onJumpAfterEvent } from "./Events/Jump Event/onJumpAfterEvent";

// new onJumpAfterEvent((data) => {
//   data.player.sendMessage("jumped");
// });
