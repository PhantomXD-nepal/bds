/**@param {Player} player  */
function saveInventory(player, invName = player.name, storage = player) {
  let { container, inventorySize } = player.getComponent("inventory");
  const items = [];
  const listOfEquipmentSlots = ["Head", "Chest", "Legs", "Feet", "Offhand"];
  let wornArmor = [];
  for (let i = 0; i < listOfEquipmentSlots.length; i++) {
    const equipment = player.getComponent("equippable").getEquipment(listOfEquipmentSlots[i]);
    if (!equipment) {
      wornArmor.push(null);
      continue;
    }
    const data = {
      typeId: equipment.typeId,
      props: {
        amount: equipment.amount,
        keepOnDeath: equipment.keepOnDeath,
        lockMode: equipment.lockMode,
      },
      lore: equipment.getLore(),
      components: {},
    };
    if (equipment.nameTag) data.props.nameTag = equipment.nameTag;
    if (equipment.hasComponent("enchantable")) {
      data.components.enchantable = equipment
        .getComponent("enchantable")
        .getEnchantments()
        .map((e) => ({ type: e.type.id, level: e.level }));
    }
    if (equipment.hasComponent("durability")) {
      data.components.durability = equipment.getComponent("durability").damage;
    }
    wornArmor.push(data);
  }
  storage.setDynamicProperty(`armor:${invName}`, JSON.stringify(wornArmor));

  for (let i = 0; i < inventorySize; i++) {
    const item = container.getItem(i);
    if (!item) {
      items.push(null);
      continue;
    }
    const data = {
      typeId: item.typeId,
      props: {
        amount: item.amount,
        keepOnDeath: item.keepOnDeath,
        lockMode: item.lockMode,
      },
      lore: item.getLore(),
      components: {},
    };
    if (item.nameTag) data.props.nameTag = item.nameTag;
    if (item.hasComponent("enchantable")) {
      data.components.enchantable = item
        .getComponent("enchantable")
        .getEnchantments()
        .map((e) => ({ type: e.type.id, level: e.level }));
    }
    if (item.hasComponent("durability")) {
      data.components.durability = item.getComponent("durability").damage;
    }
    items.push(data);
  }
  storage.setDynamicProperty(`inventory:${invName}`, JSON.stringify(items));
  return { items, wornArmor };
}

/**@param {Player} player  */
function loadInventory(player, invName = player.name, storage = player) {
  let { container, inventorySize } = player.getComponent("inventory");
  const items = JSON.parse(storage.getDynamicProperty(`inventory:${invName}`) ?? "[]");
  const wornArmor = JSON.parse(storage.getDynamicProperty(`armor:${invName}`) ?? "[]");
  const listOfEquipmentSlots = ["Head", "Chest", "Legs", "Feet", "Offhand"];
  for (let i = 0; i < listOfEquipmentSlots.length; i++) {
    const equipment = player.getComponent("equippable");
    const data = wornArmor[i];
    if (!data) {
      container.setItem(i, null);
    } else {
      const item = new ItemStack(data.typeId);
      for (const key in data.props) {
        item[key] = data.props[key];
      }
      item.setLore(data.lore);
      if (data.components.enchantable) {
        item
          .getComponent("enchantable")
          .addEnchantments(data.components.enchantable.map((e) => ({ ...e, type: new EnchantmentType(e.type) })));
      }
      if (data.components.durability) {
        item.getComponent("durability").damage = data.components.durability;
      }
      equipment.setEquipment(listOfEquipmentSlots[i], item);
    }
  }
  for (let i = 0; i < inventorySize; i++) {
    const data = items[i];
    if (!data) {
      container.setItem(i, null);
    } else {
      const item = new ItemStack(data.typeId);
      for (const key in data.props) {
        item[key] = data.props[key];
      }
      item.setLore(data.lore);
      if (data.components.enchantable) {
        item
          .getComponent("enchantable")
          .addEnchantments(data.components.enchantable.map((e) => ({ ...e, type: new EnchantmentType(e.type) })));
      }
      if (data.components.durability) {
        item.getComponent("durability").damage = data.components.durability;
      }
      container.setItem(i, item);
    }
  }
}
