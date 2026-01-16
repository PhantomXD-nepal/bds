function parseItem(json) {
  if (typeof json == "string") {
    json = JSON.parse(json);
  }

  let item = new ItemStack(json.type, json.amount);
  item.lockMode = json.lockMode;
  item.keepOnDeath = json.keepOnDeath;
  item.nameTag = json.nameTag;

  item.setCanDestroy(json.canDestroy);
  item.setCanPlaceOn(json.canPlaceOn);
  item.setLore(json.lore);

  json.properties.forEach((property) => {
    item.setDynamicProperty(property.id, property.value);
  });

  if (item.getComponent("minecraft:durability")) {
    item.getComponent("minecraft:durability").damage = json.durability;
  }

  if (item.getComponent("minecraft:enchantable")) {
    item.getComponent("minecraft:enchantable").addEnchantments(
      json.enchantments.map((enc) => {
        return {
          level: enc.level,
          type: new EnchantmentType(enc.type.id),
        };
      }),
    );
  }

  if (item.getComponent("minecraft:dyeable")) {
    item.getComponent("minecraft:dyeable").color = json.dyeColor;
  }

  return item;
}

function stringifyItem(item) {
  let json = {
    type: item.typeId,
    amount: item.amount,
    keepOnDeath: item.keepOnDeath,
    lockMode: item.lockMode,
    nameTag: item.nameTag,
    canDestroy: item.getCanDestroy(),
    canPlaceOn: item.getCanPlaceOn(),
    lore: item.getLore(),
    properties: item.getDynamicPropertyIds().map((id) => {
      return {
        id: id,
        value: item.getDynamicProperty(id),
      };
    }),
    durability: item.getComponent("minecraft:durability")?.damage,
    dyeColor: item.getComponent("minecraft:dyeable")?.color,
    enchantments: item.getComponent("minecraft:enchantable")?.getEnchantments() || [],
  };
  return JSON.stringify(json);
}
