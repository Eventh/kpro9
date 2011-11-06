"""
A module for black box testing of our program.

Should have tests for the major requirements.
"""
import sys, os
from attest import Tests, assert_hook, contexts

import csjark
import cparser
import config
import dissector

from .test_dissector import compare_lua


def create_protocols(header, yml):
    # Store default options to be able to restore them later
    config.Options.platforms = set()
    o = config.Options
    defaults = (o.verbose, o.debug, o.strict, o.use_cpp,
                o.output_dir, o.output_file, o.platforms, o.delegator)

    # Parse command line arguments
    headers, configs = csjark.parse_args(['-f', header, '-c', yml])

    # Parse config files
    for filename in configs:
        config.parse_file(filename)
    config.Options.prepare_for_parsing()

    # Create protocols
    for filename in headers:
        csjark.create_dissectors(filename)

    protocols = cparser.StructVisitor.all_protocols

    # Sort the protocols on name
    structs = {}
    for key, proto in protocols.items():
        structs[proto.name] = proto.create()

    # Write out dissectors for manual testing
    #config.Options.output_dir = os.path.dirname(__file__)
    #csjark.write_dissectors_to_file(protocols)

    # Clean up context
    config.Options.platforms = set()
    cparser.StructVisitor.all_protocols = {}
    config.Options.configs = {}
    (config.Options.verbose, config.Options.debug,
            config.Options.strict, config.Options.use_cpp,
            config.Options.output_dir, config.Options.output_file,
            config.Options.platforms, config.Options.delegator) = defaults

    return structs


# End-to-end tests for sprint 2 features
sprint2 = Tests()

@sprint2.context
def create_sprint2(structs={}):
    """Create protocols for all structs in sprint2.h"""
    if not structs:
        header = os.path.join(os.path.dirname(__file__), 'sprint2.h')
        yml = os.path.join(os.path.dirname(__file__), 'sprint2.yml')
        structs.update(create_protocols(header, yml))
    yield structs


@sprint2.test
def cenums(structs):
    """End-to-end test headers with C enums in them."""
    assert 'cenum_test' in structs
    assert structs['cenum_test']
    assert compare_lua(structs['cenum_test'], '''
-- Dissector for default.cenum_test: C Enum test (default)
local proto_cenum_test = Proto("default.cenum_test", "C Enum test (default)")
-- ProtoField defintions for: cenum_test
local f = proto_cenum_test.fields
f.id = ProtoField.int32("cenum_test.id", "id")
local mnd_values = {[1]="JAN", [2]="FEB", [3]="MAR", [4]="APR", [5]="MAY", [6]="JUN", [7]="JUL", [8]="AUG", [9]="SEP", [10]="OCT", [11]="NOV", [20]="DEC"}
f.mnd = ProtoField.uint32("cenum_test.mnd", "mnd", nil, mnd_values)
-- Dissector function for: cenum_test
function proto_cenum_test.dissector(buffer, pinfo, tree)
local subtree = tree:add(proto_cenum_test, buffer())
if pinfo.private.caller_def_name then
subtree:set_text(pinfo.private.caller_def_name .. ": cenum_test")
pinfo.private.caller_def_name = nil
else
pinfo.cols.info:append(" (" .. proto_cenum_test.description .. ")")
end
subtree:add(f.id, buffer(0, 4))
local mnd = subtree:add(f.mnd, buffer(4, 4))
if (mnd_values[buffer(4, 4):uint()] == nil) then
mnd:add_expert_info(PI_MALFORMED, PI_WARN, "Invalid value, not in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 20)")
end
end
delegator_register_proto(proto_cenum_test, "default", "cenum_test", 11)
''')


@sprint2.test
def arrays(structs):
    """End-to-end test headers with arrays in them."""
    assert 'array_test' in structs
    assert structs['array_test']
    assert compare_lua(structs['array_test'], '''
-- Dissector for default.array_test: Multidimensional array (default)
local proto_array_test = Proto("default.array_test", "Multidimensional array (default)")
-- ProtoField defintions for: array_test
local f = proto_array_test.fields
f.chararr1 = ProtoField.string("array_test.chararr1", "chararr1")
-- Array definition for intarr2
f.intarr2 = ProtoField.bytes("array_test.intarr2", "intarr2")
f.intarr2_0 = ProtoField.bytes("array_test.intarr2_0", "intarr2")
f.intarr2_0_0 = ProtoField.int32("array_test.intarr2_0_0", "intarr2[0][0]")
f.intarr2_0_1 = ProtoField.int32("array_test.intarr2_0_1", "intarr2[0][1]")
f.intarr2_0_2 = ProtoField.int32("array_test.intarr2_0_2", "intarr2[0][2]")
f.intarr2_0_3 = ProtoField.int32("array_test.intarr2_0_3", "intarr2[0][3]")
f.intarr2_1 = ProtoField.bytes("array_test.intarr2_1", "intarr2")
f.intarr2_1_0 = ProtoField.int32("array_test.intarr2_1_0", "intarr2[1][0]")
f.intarr2_1_1 = ProtoField.int32("array_test.intarr2_1_1", "intarr2[1][1]")
f.intarr2_1_2 = ProtoField.int32("array_test.intarr2_1_2", "intarr2[1][2]")
f.intarr2_1_3 = ProtoField.int32("array_test.intarr2_1_3", "intarr2[1][3]")
f.intarr2_2 = ProtoField.bytes("array_test.intarr2_2", "intarr2")
f.intarr2_2_0 = ProtoField.int32("array_test.intarr2_2_0", "intarr2[2][0]")
f.intarr2_2_1 = ProtoField.int32("array_test.intarr2_2_1", "intarr2[2][1]")
f.intarr2_2_2 = ProtoField.int32("array_test.intarr2_2_2", "intarr2[2][2]")
f.intarr2_2_3 = ProtoField.int32("array_test.intarr2_2_3", "intarr2[2][3]")
f.intarr2_3 = ProtoField.bytes("array_test.intarr2_3", "intarr2")
f.intarr2_3_0 = ProtoField.int32("array_test.intarr2_3_0", "intarr2[3][0]")
f.intarr2_3_1 = ProtoField.int32("array_test.intarr2_3_1", "intarr2[3][1]")
f.intarr2_3_2 = ProtoField.int32("array_test.intarr2_3_2", "intarr2[3][2]")
f.intarr2_3_3 = ProtoField.int32("array_test.intarr2_3_3", "intarr2[3][3]")
-- Array definition for chararr3
f.chararr3 = ProtoField.string("array_test.chararr3", "chararr3")
f.chararr3_0 = ProtoField.string("array_test.chararr3_0", "chararr3[0]")
f.chararr3_1 = ProtoField.string("array_test.chararr3_1", "chararr3[1]")
-- Array definition for floatarr4
f.floatarr4 = ProtoField.bytes("array_test.floatarr4", "floatarr4")
f.floatarr4_0 = ProtoField.bytes("array_test.floatarr4_0", "floatarr4")
f.floatarr4_0_0 = ProtoField.float("array_test.floatarr4_0_0", "floatarr4[0][0]")
f.floatarr4_0_1 = ProtoField.float("array_test.floatarr4_0_1", "floatarr4[0][1]")
f.floatarr4_1 = ProtoField.bytes("array_test.floatarr4_1", "floatarr4")
f.floatarr4_1_0 = ProtoField.float("array_test.floatarr4_1_0", "floatarr4[1][0]")
f.floatarr4_1_1 = ProtoField.float("array_test.floatarr4_1_1", "floatarr4[1][1]")
f.floatarr4_2 = ProtoField.bytes("array_test.floatarr4_2", "floatarr4")
f.floatarr4_2_0 = ProtoField.float("array_test.floatarr4_2_0", "floatarr4[2][0]")
f.floatarr4_2_1 = ProtoField.float("array_test.floatarr4_2_1", "floatarr4[2][1]")
-- Dissector function for: array_test
function proto_array_test.dissector(buffer, pinfo, tree)
local subtree = tree:add(proto_array_test, buffer())
if pinfo.private.caller_def_name then
subtree:set_text(pinfo.private.caller_def_name .. ": array_test")
pinfo.private.caller_def_name = nil
else
pinfo.cols.info:append(" (" .. proto_array_test.description .. ")")
end
subtree:add(f.chararr1, buffer(0, 16))
-- Array handling for intarr2
local arraytree = subtree:add("intarr2: int32 array", buffer(16, 64))
local subarraytree = arraytree:add("intarr2[0]: int32 array", buffer(16, 16))
subarraytree:add(f.intarr2_0_0, buffer(16, 4))
subarraytree:add(f.intarr2_0_1, buffer(20, 4))
subarraytree:add(f.intarr2_0_2, buffer(24, 4))
subarraytree:add(f.intarr2_0_3, buffer(28, 4))
local subarraytree = arraytree:add("intarr2[1]: int32 array", buffer(32, 16))
subarraytree:add(f.intarr2_1_0, buffer(32, 4))
subarraytree:add(f.intarr2_1_1, buffer(36, 4))
subarraytree:add(f.intarr2_1_2, buffer(40, 4))
subarraytree:add(f.intarr2_1_3, buffer(44, 4))
local subarraytree = arraytree:add("intarr2[2]: int32 array", buffer(48, 16))
subarraytree:add(f.intarr2_2_0, buffer(48, 4))
subarraytree:add(f.intarr2_2_1, buffer(52, 4))
subarraytree:add(f.intarr2_2_2, buffer(56, 4))
subarraytree:add(f.intarr2_2_3, buffer(60, 4))
local subarraytree = arraytree:add("intarr2[3]: int32 array", buffer(64, 16))
subarraytree:add(f.intarr2_3_0, buffer(64, 4))
subarraytree:add(f.intarr2_3_1, buffer(68, 4))
subarraytree:add(f.intarr2_3_2, buffer(72, 4))
subarraytree:add(f.intarr2_3_3, buffer(76, 4))
-- Array handling for chararr3
local arraytree = subtree:add("chararr3: string array", buffer(80, 6))
arraytree:add(f.chararr3_0, buffer(80, 3))
arraytree:add(f.chararr3_1, buffer(83, 3))
-- Array handling for floatarr4
local arraytree = subtree:add("floatarr4: float array", buffer(88, 24))
local subarraytree = arraytree:add("floatarr4[0]: float array", buffer(88, 8))
subarraytree:add(f.floatarr4_0_0, buffer(88, 4))
subarraytree:add(f.floatarr4_0_1, buffer(92, 4))
local subarraytree = arraytree:add("floatarr4[1]: float array", buffer(96, 8))
subarraytree:add(f.floatarr4_1_0, buffer(96, 4))
subarraytree:add(f.floatarr4_1_1, buffer(100, 4))
local subarraytree = arraytree:add("floatarr4[2]: float array", buffer(104, 8))
subarraytree:add(f.floatarr4_2_0, buffer(104, 4))
subarraytree:add(f.floatarr4_2_1, buffer(108, 4))
end
delegator_register_proto(proto_array_test, "default", "array_test", 16)
''')


@sprint2.test
def bitstrings(structs):
    """End-to-end test headers with bitstrings in them."""
    assert 'bitstring_test' in structs
    assert structs['bitstring_test']
    assert compare_lua(structs['bitstring_test'], '''
-- Dissector for default.bitstring_test: Bit string test (default)
local proto_bitstring_test = Proto("default.bitstring_test", "Bit string test (default)")
-- ProtoField defintions for: bitstring_test
local f = proto_bitstring_test.fields
f.id = ProtoField.int32("bitstring_test.id", "id")
-- Bitstring definitions for flags
f.flags = ProtoField.uint32("bitstring_test.flags", "flags (bitstring)", base.HEX)
f.flags_inuse = ProtoField.uint32("bitstring_test.flags.In_use", "In use", nil, {[0]="No", [1]="Yes"}, 0x1)
f.flags_endian = ProtoField.uint32("bitstring_test.flags.Endian", "Endian", nil, {[0]="Big", [1]="Little"}, 0x2)
f.flags_platform = ProtoField.uint32("bitstring_test.flags.Platform", "Platform", nil, {[0]="Win", [1]="Linux", [2]="Mac", [3]="Solaris"}, 0xc)
f.flags_test = ProtoField.uint32("bitstring_test.flags.Test", "Test", nil, {[0]="No", [1]="Yes"}, 0x10)
-- Bitstring definitions for color1
f.color1 = ProtoField.uint16("bitstring_test.color1", "color1 (bitstring)", base.HEX)
f.color1_red = ProtoField.uint16("bitstring_test.color1.RED", "RED", nil, {[0]="No", [1]="Yes"}, 0x1)
f.color1_blue = ProtoField.uint16("bitstring_test.color1.Blue", "Blue", nil, {[0]="No", [1]="Yes"}, 0x2)
f.color1_green = ProtoField.uint16("bitstring_test.color1.Green", "Green", nil, {[0]="No", [1]="Yes"}, 0x4)
-- Bitstring definitions for color2
f.color2 = ProtoField.uint16("bitstring_test.color2", "color2 (bitstring)", base.HEX)
f.color2_red = ProtoField.uint16("bitstring_test.color2.RED", "RED", nil, {[0]="No", [1]="Yes"}, 0x1)
f.color2_blue = ProtoField.uint16("bitstring_test.color2.Blue", "Blue", nil, {[0]="No", [1]="Yes"}, 0x2)
f.color2_green = ProtoField.uint16("bitstring_test.color2.Green", "Green", nil, {[0]="No", [1]="Yes"}, 0x4)
-- Dissector function for: bitstring_test
function proto_bitstring_test.dissector(buffer, pinfo, tree)
	local subtree = tree:add(proto_bitstring_test, buffer())
	if pinfo.private.caller_def_name then
		subtree:set_text(pinfo.private.caller_def_name .. ": bitstring_test")
		pinfo.private.caller_def_name = nil
	else
		pinfo.cols.info:append(" (" .. proto_bitstring_test.description .. ")")
	end
	subtree:add(f.id, buffer(0, 4))
	-- Bitstring handling for flags
	local bittree = subtree:add(f.flags, buffer(4, 4))
	bittree:add(f.flags_inuse, buffer(4, 4))
	bittree:add(f.flags_endian, buffer(4, 4))
	bittree:add(f.flags_platform, buffer(4, 4))
	bittree:add(f.flags_test, buffer(4, 4))
	-- Bitstring handling for color1
	local bittree = subtree:add(f.color1, buffer(8, 2))
	bittree:add(f.color1_red, buffer(8, 2))
	bittree:add(f.color1_blue, buffer(8, 2))
	bittree:add(f.color1_green, buffer(8, 2))
	-- Bitstring handling for color2
	local bittree = subtree:add(f.color2, buffer(10, 2))
	bittree:add(f.color2_red, buffer(10, 2))
	bittree:add(f.color2_blue, buffer(10, 2))
	bittree:add(f.color2_green, buffer(10, 2))
end
delegator_register_proto(proto_bitstring_test, "default", "bitstring_test", 13)
''')


@sprint2.test
def custom(structs):
    """End-to-end test headers with custom field rules."""
    assert 'custom_lua' in structs
    assert structs['custom_lua']
    assert compare_lua(structs['custom_lua'], '''
-- Dissector for default.custom_lua: custom_lua (default)
local proto_custom_lua = Proto("default.custom_lua", "custom_lua (default)")
-- ProtoField defintions for: custom_lua
local f = proto_custom_lua.fields
f.normal = ProtoField.int16("custom_lua.normal", "normal")
f.special = ProtoField.int64("custom_lua.special", "special")
f.abs = ProtoField.absolute_time("custom_lua.abs", "abs")
f.rel = ProtoField.relative_time("custom_lua.rel", "rel")
f.bol = ProtoField.bool("bool", "bol")
f.all = ProtoField.uint32("all.all", "all", base.HEX, {[0]="Monday", [1]="Tuesday"}, nil, "This is something dark side!")
local truth_values = {[0]="TRUE", [1]="FALSE"}
f.truth = ProtoField.uint32("custom_lua.truth", "truth", nil, truth_values)
-- Array definition for five
f.five = ProtoField.bytes("custom_lua.five", "five")
f.five_0 = ProtoField.int32("custom_lua.five_0", "five[0]")
f.five_1 = ProtoField.int32("custom_lua.five_1", "five[1]")
f.five_2 = ProtoField.int32("custom_lua.five_2", "five[2]")
f.five_3 = ProtoField.int32("custom_lua.five_3", "five[3]")
f.five_4 = ProtoField.int32("custom_lua.five_4", "five[4]")
f.pointer = ProtoField.int32("custom_lua.pointer", "pointer")
-- Array definition for str
f.str = ProtoField.string("custom_lua.str", "str")
f.str_0 = ProtoField.string("custom_lua.str_0", "str")
f.str_0_0 = ProtoField.string("custom_lua.str_0_0", "str[0][0]")
f.str_0_1 = ProtoField.string("custom_lua.str_0_1", "str[0][1]")
f.str_0_2 = ProtoField.string("custom_lua.str_0_2", "str[0][2]")
f.str_0_3 = ProtoField.string("custom_lua.str_0_3", "str[0][3]")
f.str_1 = ProtoField.string("custom_lua.str_1", "str")
f.str_1_0 = ProtoField.string("custom_lua.str_1_0", "str[1][0]")
f.str_1_1 = ProtoField.string("custom_lua.str_1_1", "str[1][1]")
f.str_1_2 = ProtoField.string("custom_lua.str_1_2", "str[1][2]")
f.str_1_3 = ProtoField.string("custom_lua.str_1_3", "str[1][3]")
f.str_2 = ProtoField.string("custom_lua.str_2", "str")
f.str_2_0 = ProtoField.string("custom_lua.str_2_0", "str[2][0]")
f.str_2_1 = ProtoField.string("custom_lua.str_2_1", "str[2][1]")
f.str_2_2 = ProtoField.string("custom_lua.str_2_2", "str[2][2]")
f.str_2_3 = ProtoField.string("custom_lua.str_2_3", "str[2][3]")
-- Dissector function for: custom_lua
function proto_custom_lua.dissector(buffer, pinfo, tree)
local subtree = tree:add(proto_custom_lua, buffer())
if pinfo.private.caller_def_name then
subtree:set_text(pinfo.private.caller_def_name .. ": custom_lua")
pinfo.private.caller_def_name = nil
else
pinfo.cols.info:append(" (" .. proto_custom_lua.description .. ")")
end
subtree:add(f.normal, buffer(0, 2))
subtree:add(f.special, buffer(8, 8))
subtree:add(f.abs, buffer(16, 4))
subtree:add(f.rel, buffer(20, 4))
subtree:add(f.bol, buffer(24, 4))
subtree:add(f.all, buffer(28, 4))
local truth = subtree:add(f.truth, buffer(32, 4))
if (truth_values[buffer(32, 4):uint()] == nil) then
truth:add_expert_info(PI_MALFORMED, PI_WARN, "Invalid value, not in (0, 1)")
end
-- Array handling for five
local arraytree = subtree:add("five: int32 array", buffer(36, 20))
arraytree:add(f.five_0, buffer(36, 4))
arraytree:add(f.five_1, buffer(40, 4))
arraytree:add(f.five_2, buffer(44, 4))
arraytree:add(f.five_3, buffer(48, 4))
arraytree:add(f.five_4, buffer(52, 4))
subtree:add(f.pointer, buffer(56, 4))
-- Array handling for str
local arraytree = subtree:add("str: string array", buffer(60, 24))
local subarraytree = arraytree:add("str[0]: string array", buffer(60, 8))
subarraytree:add(f.str_0_0, buffer(60, 2))
subarraytree:add(f.str_0_1, buffer(62, 2))
subarraytree:add(f.str_0_2, buffer(64, 2))
subarraytree:add(f.str_0_3, buffer(66, 2))
local subarraytree = arraytree:add("str[1]: string array", buffer(68, 8))
subarraytree:add(f.str_1_0, buffer(68, 2))
subarraytree:add(f.str_1_1, buffer(70, 2))
subarraytree:add(f.str_1_2, buffer(72, 2))
subarraytree:add(f.str_1_3, buffer(74, 2))
local subarraytree = arraytree:add("str[2]: string array", buffer(76, 8))
subarraytree:add(f.str_2_0, buffer(76, 2))
subarraytree:add(f.str_2_1, buffer(78, 2))
subarraytree:add(f.str_2_2, buffer(80, 2))
subarraytree:add(f.str_2_3, buffer(82, 2))
end
delegator_register_proto(proto_custom_lua, "default", "custom_lua", 74)
''')


@sprint2.test
def enums(structs):
    """End-to-end test headers with enums in them."""
    assert 'enum_test' in structs
    assert structs['enum_test']
    assert compare_lua(structs['enum_test'], '''
-- Dissector for default.enum_test: Enum config test (default)
local proto_enum_test = Proto("default.enum_test", "Enum config test (default)")
-- ProtoField defintions for: enum_test
local f = proto_enum_test.fields
local id_values = {[0]="Zero", [1]="One", [2]="Two", [3]="Three", [4]="Four", [5]="Five"}
f.id = ProtoField.int32("enum_test.id", "id", nil, id_values)
f.name = ProtoField.string("enum_test.name", "name")
local weekday_values = {[1]="MONDAY", [2]="TUESDAY", [3]="WEDNESDAY", [4]="THURSDAY", [5]="FRIDAY", [6]="SATURDAY", [7]="SUNDAY"}
f.weekday = ProtoField.int32("enum_test.weekday", "weekday", nil, weekday_values)
local number_values = {[0]="Zero", [1]="One", [2]="Two", [3]="Three", [4]="Four", [5]="Five"}
f.number = ProtoField.int32("enum_test.number", "number", nil, number_values)
-- Dissector function for: enum_test
function proto_enum_test.dissector(buffer, pinfo, tree)
	local subtree = tree:add(proto_enum_test, buffer())
	if pinfo.private.caller_def_name then
		subtree:set_text(pinfo.private.caller_def_name .. ": enum_test")
		pinfo.private.caller_def_name = nil
	else
		pinfo.cols.info:append(" (" .. proto_enum_test.description .. ")")
	end
	local id = subtree:add(f.id, buffer(0, 4))
	if (id_values[buffer(0, 4):int()] == nil) then
		id:add_expert_info(PI_MALFORMED, PI_WARN, "Invalid value, not in (0, 1, 2, 3, 4, 5)")
	end
	subtree:add(f.name, buffer(4, 10))
	local weekday = subtree:add(f.weekday, buffer(16, 4))
	if (weekday_values[buffer(16, 4):int()] == nil) then
		weekday:add_expert_info(PI_MALFORMED, PI_WARN, "Invalid value, not in (1, 2, 3, 4, 5, 6, 7)")
	end
	local number = subtree:add(f.number, buffer(20, 4))
	if (number_values[buffer(20, 4):int()] == nil) then
		number:add_expert_info(PI_MALFORMED, PI_WARN, "Invalid value, not in (0, 1, 2, 3, 4, 5)")
	end
end
delegator_register_proto(proto_enum_test, "default", "enum_test", 10)
''')


@sprint2.test
def ranges(structs):
    """End-to-end test headers with ranges in them."""
    assert 'range_test' in structs
    assert structs['range_test']
    assert compare_lua(structs['range_test'], '''
-- Dissector for default.range_test: Range rules test (default)
local proto_range_test = Proto("default.range_test", "Range rules test (default)")
-- ProtoField defintions for: range_test
local f = proto_range_test.fields
f.name = ProtoField.string("range_test.name", "name")
f.age = ProtoField.int32("range_test.age", "age")
-- Dissector function for: range_test
function proto_range_test.dissector(buffer, pinfo, tree)
	local subtree = tree:add(proto_range_test, buffer())
	if pinfo.private.caller_def_name then
		subtree:set_text(pinfo.private.caller_def_name .. ": range_test")
		pinfo.private.caller_def_name = nil
	else
		pinfo.cols.info:append(" (" .. proto_range_test.description .. ")")
	end
	subtree:add(f.name, buffer(0, 10))
	local age = subtree:add(f.age, buffer(12, 4))
	if (buffer(12, 4):int() < 0.0) then
		age:add_expert_info(PI_MALFORMED, PI_WARN, "Should be larger than 0.0")
	end
	if (buffer(12, 4):int() > 100.0) then
		age:add_expert_info(PI_MALFORMED, PI_WARN, "Should be smaller than 100.0")
	end
end
delegator_register_proto(proto_range_test, "default", "range_test", 9)
''')


@sprint2.test
def struct_within_struct(structs):
    """End-to-end test of structs within structs."""
    assert 'struct_within_struct_test' in structs
    assert structs['struct_within_struct_test']
    assert compare_lua(structs['struct_within_struct_test'], '''
-- Dissector for default.struct_within_struct_test: Struct in struct test (default)
local proto_struct_within_struct_test = Proto("default.struct_within_struct_test", "Struct in struct test (default)")
-- ProtoField defintions for: struct_within_struct_test
local f = proto_struct_within_struct_test.fields
f.prime = ProtoField.int32("struct_within_struct_test.prime", "prime")
-- Dissector function for: struct_within_struct_test
function proto_struct_within_struct_test.dissector(buffer, pinfo, tree)
local subtree = tree:add(proto_struct_within_struct_test, buffer())
if pinfo.private.caller_def_name then
subtree:set_text(pinfo.private.caller_def_name .. ": struct_within_struct_test")
pinfo.private.caller_def_name = nil
else
pinfo.cols.info:append(" (" .. proto_struct_within_struct_test.description .. ")")
end
subtree:add(f.prime, buffer(0, 4))
pinfo.private.caller_def_name = "astruct"
Dissector.get("default.cenum_test"):call(buffer(4,8):tvb(), pinfo, subtree)
end
delegator_register_proto(proto_struct_within_struct_test, "default", "struct_within_struct_test", 12)
''')


@sprint2.test
def trailers(structs):
    """End-to-end test headers with trailers in them."""
    assert 'trailer_test' in structs
    assert structs['trailer_test']
    assert compare_lua(structs['trailer_test'], '''
-- Dissector for default.trailer_test: trailer_test (default)
local proto_trailer_test = Proto("default.trailer_test", "trailer_test (default)
")

-- ProtoField defintions for: trailer_test
local f = proto_trailer_test.fields
-- Array definition for tmp
f.tmp = ProtoField.bytes("trailer_test.tmp", "tmp")
f.tmp_0 = ProtoField.float("trailer_test.tmp_0", "tmp[0]")
f.tmp_1 = ProtoField.float("trailer_test.tmp_1", "tmp[1]")
f.tmp_2 = ProtoField.float("trailer_test.tmp_2", "tmp[2]")
f.tmp_3 = ProtoField.float("trailer_test.tmp_3", "tmp[3]")
f.tmp_4 = ProtoField.float("trailer_test.tmp_4", "tmp[4]")
f.asn1_count = ProtoField.int32("trailer_test.asn1_count", "asn1_count")
-- Dissector function for: trailer_test
function proto_trailer_test.dissector(buffer, pinfo, tree)
local subtree = tree:add(proto_trailer_test, buffer())
if pinfo.private.caller_def_name then
subtree:set_text(pinfo.private.caller_def_name .. ": trailer_test")
pinfo.private.caller_def_name = nil
else
pinfo.cols.info:append(" (" .. proto_trailer_test.description ..")")
end
-- Array handling for tmp
local arraytree = subtree:add("tmp: float array", buffer(0, 20))
arraytree:add(f.tmp_0, buffer(0, 4))
arraytree:add(f.tmp_1, buffer(4, 4))
arraytree:add(f.tmp_2, buffer(8, 4))
arraytree:add(f.tmp_3, buffer(12, 4))
arraytree:add(f.tmp_4, buffer(16, 4))
subtree:add(f.asn1_count, buffer(20, 4))
-- Trailers handling for struct: trailer_test
local trail_offset = 24
local trail_count = buffer(20, 4):int()
for i = 1, trail_count do
local trailer = Dissector.get("ber")
trailer:call(buffer(trail_offset, 6):tvb(), pinfo, tree)
trail_offset = trail_offset + 6
end
local trailer = Dissector.get("ber")
trailer:call(buffer(trail_offset, 5):tvb(), pinfo, tree)
trail_offset = trail_offset + 5
for i = 1, 2 do
local trailer = Dissector.get("ber")
trailer:call(buffer(trail_offset, 6):tvb(), pinfo, tree)
trail_offset = trail_offset + 6
end
local trailer = Dissector.get("ber")
trailer:call(buffer(trail_offset):tvb(), pinfo, tree)
end
delegator_register_proto(proto_trailer_test, "default", "trailer_test", 66)
''')


# End-to-end tests for sprint 3 features
sprint3 = Tests()

@sprint3.context
def create_sprint3(structs={}):
    """Create protocols for all structs in sprint2.h"""
    if not structs:
        header = os.path.join(os.path.dirname(__file__), 'sprint3.h')
        yml = os.path.join(os.path.dirname(__file__), 'sprint3.yml')
        structs.update(create_protocols(header, yml))
    yield structs


@sprint3.test
def keywords(structs):
    """End-to-end test headers with lua reserved keywords in them."""
    assert 'keyword_test' in structs
    assert structs['keyword_test']
    assert compare_lua(structs['keyword_test'], '''
-- Dissector for win32.keyword_test: testing lua keywords (Win32)
local proto_keyword_test = Proto("win32.keyword_test", "testing lua keywords (Win32)")
-- ProtoField defintions for: keyword_test
local f = proto_keyword_test.fields
f._in = ProtoField.int32("keyword_test.in", "in")
-- Array definition for until
f._until = ProtoField.bytes("keyword_test.until", "until")
f._until_0 = ProtoField.bytes("keyword_test.until_0", "until")
f._until_0_0 = ProtoField.int32("keyword_test.until_0_0", "until[0][0]")
f._until_0_1 = ProtoField.int32("keyword_test.until_0_1", "until[0][1]")
f._until_1 = ProtoField.bytes("keyword_test.until_1", "until")
f._until_1_0 = ProtoField.int32("keyword_test.until_1_0", "until[1][0]")
f._until_1_1 = ProtoField.int32("keyword_test.until_1_1", "until[1][1]")
-- Bitstring definitions for _VERSION
f._version = ProtoField.uint32("keyword_test._VERSION", "_VERSION (bitstring)", base.HEX)
f._version_g1 = ProtoField.uint32("keyword_test._VERSION.G1", "G1", nil, {[0]="True", [1]="False"}, 0x1)
local function_values = {[1]="and", [2]="elseif", [412]="in"}
f._function = ProtoField.uint32("keyword_test.function", "function", nil, function_values)
f._and = ProtoField.int32("keyword_test.and", "and")
f._and = ProtoField.int32("keyword_test._and", "_and")
f._not = ProtoField.int32("keyword_test.not", "not")
-- Dissector function for: keyword_test
function proto_keyword_test.dissector(buffer, pinfo, tree)
local subtree = tree:add_le(proto_keyword_test, buffer())
if pinfo.private.caller_def_name then
subtree:set_text(pinfo.private.caller_def_name .. ": keyword_test")
pinfo.private.caller_def_name = nil
else
pinfo.cols.info:append(" (" .. proto_keyword_test.description .. ")")
end
local _in = subtree:add_le(f._in, buffer(0, 4))
if (buffer(0, 4):le_int() < 0.0) then
_in:add_expert_info(PI_MALFORMED, PI_WARN, "Should be larger than 0.0")
end
if (buffer(0, 4):le_int() > 10.0) then
_in:add_expert_info(PI_MALFORMED, PI_WARN, "Should be smaller than 10.0")
end
-- Array handling for until
local arraytree = subtree:add_le("until: int32 array", buffer(4, 16))
local subarraytree = arraytree:add_le("until[0]: int32 array", buffer(4, 8))
subarraytree:add_le(f._until_0_0, buffer(4, 4))
subarraytree:add_le(f._until_0_1, buffer(8, 4))
local subarraytree = arraytree:add_le("until[1]: int32 array", buffer(12, 8))
subarraytree:add_le(f._until_1_0, buffer(12, 4))
subarraytree:add_le(f._until_1_1, buffer(16, 4))
-- Bitstring handling for _VERSION
local bittree = subtree:add_le(f._version, buffer(20, 4))
bittree:add_le(f._version_g1, buffer(20, 4))
local _function = subtree:add_le(f._function, buffer(24, 4))
if (function_values[buffer(24, 4):le_uint()] == nil) then
_function:add_expert_info(PI_MALFORMED, PI_WARN, "Invalid value, not in (1, 2, 412)")
end
pinfo.private.caller_def_name = "or"
Dissector.get("win32.local"):call(buffer(28,4):tvb(), pinfo, subtree)
subtree:add_le(f._and, buffer(32, 4))
subtree:add_le(f._and, buffer(36, 4))
subtree:add_le(f._not, buffer(40, 4))
-- Trailers handling for struct: keyword_test
local trail_offset = 44
local trail_count = buffer(40, 4):le_int()
for i = 1, trail_count do
local trailer = Dissector.get("ber")
trailer:call(buffer(trail_offset, 5):tvb(), pinfo, tree)
end
end
delegator_register_proto(proto_keyword_test, "Win32", "keyword_test", 255)
''')


@sprint3.test
def platforms(structs):
    """End-to-end test platform specific header."""
    assert 'platform_test' in structs
    assert structs['platform_test']
    assert compare_lua(structs['platform_test'], '''
-- Dissector for win32.platform_test: platform_test (Win32)
local proto_platform_test = Proto("win32.platform_test", "platform_test (Win32)")
-- ProtoField defintions for: platform_test
local f = proto_platform_test.fields
f.bytes = ProtoField.bytes("platform_test.bytes", "bytes")
f.a = ProtoField.int32("platform_test.a", "a")
f.win_float = ProtoField.float("platform_test.win_float", "win_float")
f.b = ProtoField.int8("platform_test.b", "b")
f.deff = ProtoField.int64("platform_test.deff", "deff")
f.intel = ProtoField.int64("platform_test.intel", "intel")
-- Dissector function for: platform_test
function proto_platform_test.dissector(buffer, pinfo, tree)
local subtree = tree:add_le(proto_platform_test, buffer())
if pinfo.private.caller_def_name then
subtree:set_text(pinfo.private.caller_def_name .. ": platform_test")
pinfo.private.caller_def_name = nil
else
pinfo.cols.info:append(" (" .. proto_platform_test.description .. ")")
end
subtree:add_le(f.bytes, buffer(0, 8))
subtree:add_le(f.a, buffer(8, 4))
subtree:add_le(f.win_float, buffer(12, 4))
subtree:add_le(f.b, buffer(16, 1))
pinfo.private.caller_def_name = "anom"
Dissector.get("win32.anom"):call(buffer(20,4):tvb(), pinfo, subtree)
subtree:add_le(f.deff, buffer(24, 4))
subtree:add_le(f.intel, buffer(28, 4))
end
delegator_register_proto(proto_platform_test, "Win32", "platform_test", 670)
''')


@sprint3.test
def unions(structs):
    """End-to-end test platform specific header."""
    assert 'union_test' in structs
    assert structs['union_test']
    assert compare_lua(structs['union_test'], '''
-- Dissector for win32.union_test: Test for union_test (Win32)
local proto_union_test = Proto("win32.union_test", "Test for union_test (Win32)")
-- ProtoField defintions for: union_test
local f = proto_union_test.fields
f.int_member = ProtoField.int32("union_test.int_member", "int_member")
f.float_member = ProtoField.float("union_test.float_member", "float_member")
f.long_long_member = ProtoField.uint64("union_test.long_long_member", "long_long_member")
-- Dissector function for: union_test
function proto_union_test.dissector(buffer, pinfo, tree)
local subtree = tree:add_le(proto_union_test, buffer())
if pinfo.private.caller_def_name then
subtree:set_text(pinfo.private.caller_def_name .. ": union_test")
pinfo.private.caller_def_name = nil
else
pinfo.cols.info:append(" (" .. proto_union_test.description .. ")")
end
subtree:add_le(f.int_member, buffer(0, 4))
subtree:add_le(f.float_member, buffer(0, 4))
subtree:add_le(f.long_long_member, buffer(0, 8))
end
delegator_register_proto(proto_union_test, "Win32", "union_test", 161)
''')


@sprint3.test
def conformance_files(structs):
    """End-to-end test conformance-files."""
    assert 'custom_lua' in structs
    assert structs['custom_lua']
    assert compare_lua(structs['custom_lua'], '''
-- Dissector for win32.custom_lua: custom_lua (Win32)
local proto_custom_lua = Proto("win32.custom_lua", "custom_lua (Win32)")
-- ProtoField defintions for: custom_lua
local f = proto_custom_lua.fields
f.normal = ProtoField.int16("custom_lua.normal", "normal")
f.special = ProtoField.int64("custom_lua.special", "special")
f.abs = ProtoField.absolute_time("custom_lua.abs", "abs")
f.rel = ProtoField.relative_time("custom_lua.rel", "rel")
f.bol = ProtoField.bool("bool", "bol")
f.all = ProtoField.uint32("all.all", "all", base.HEX, {[0]="Monday", [1]="Tuesday"}, nil, "This is something dark side!")
-- This is above 'truth'
local truth_values = {[0]="TRUE", [1]="FALSE"}
f.truth = ProtoField.uint32("custom_lua.truth", "truth", nil, truth_values)
-- This is below
-- Array definition for five
f.five = ProtoField.bytes("custom_lua.five", "five")
f.five_0 = ProtoField.int32("custom_lua.five_0", "five[0]")
f.five_1 = ProtoField.int32("custom_lua.five_1", "five[1]")
f.five_2 = ProtoField.int32("custom_lua.five_2", "five[2]")
f.five_3 = ProtoField.int32("custom_lua.five_3", "five[3]")
f.five_4 = ProtoField.int32("custom_lua.five_4", "five[4]")
f.pointer = ProtoField.int32("custom_lua.pointer", "pointer")
-- This is below 'pointer'
-- Array definition for str
f.str = ProtoField.string("custom_lua.str", "str")
f.str_0 = ProtoField.string("custom_lua.str_0", "str")
f.str_0_0 = ProtoField.string("custom_lua.str_0_0", "str[0][0]")
f.str_0_1 = ProtoField.string("custom_lua.str_0_1", "str[0][1]")
f.str_0_2 = ProtoField.string("custom_lua.str_0_2", "str[0][2]")
f.str_0_3 = ProtoField.string("custom_lua.str_0_3", "str[0][3]")
f.str_1 = ProtoField.string("custom_lua.str_1", "str")
f.str_1_0 = ProtoField.string("custom_lua.str_1_0", "str[1][0]")
f.str_1_1 = ProtoField.string("custom_lua.str_1_1", "str[1][1]")
f.str_1_2 = ProtoField.string("custom_lua.str_1_2", "str[1][2]")
f.str_1_3 = ProtoField.string("custom_lua.str_1_3", "str[1][3]")
f.str_2 = ProtoField.string("custom_lua.str_2", "str")
f.str_2_0 = ProtoField.string("custom_lua.str_2_0", "str[2][0]")
f.str_2_1 = ProtoField.string("custom_lua.str_2_1", "str[2][1]")
f.str_2_2 = ProtoField.string("custom_lua.str_2_2", "str[2][2]")
f.str_2_3 = ProtoField.string("custom_lua.str_2_3", "str[2][3]")
-- This was all the field defintions
-- Dissector function for: custom_lua
function proto_custom_lua.dissector(buffer, pinfo, tree)
local subtree = tree:add_le(proto_custom_lua, buffer())
if pinfo.private.caller_def_name then
subtree:set_text(pinfo.private.caller_def_name .. ": custom_lua")
pinfo.private.caller_def_name = nil
else
pinfo.cols.info:append(" (" .. proto_custom_lua.description .. ")")
end
subtree:add_le(f.normal, buffer(0, 2))
subtree:add_le(f.special, buffer(8, 8))
subtree:add_le(f.abs, buffer(16, 4))
subtree:add_le(f.rel, buffer(20, 4))
subtree:add_le(f.bol, buffer(24, 4))
subtree:add_le(f.all, buffer(28, 4))
-- This is above 'truth' inside the dissector function.
local truth = subtree:add_le(f.truth, buffer(32, 4))
if (truth_values[buffer(32, 4):le_uint()] == nil) then
truth:add_expert_info(PI_MALFORMED, PI_WARN, "Invalid value, not in (0, 1)")
end
-- Array handling for five
local arraytree = subtree:add_le("five: int32 array", buffer(36, 20))
arraytree:add_le(f.five_0, buffer(36, 4))
arraytree:add_le(f.five_1, buffer(40, 4))
arraytree:add_le(f.five_2, buffer(44, 4))
arraytree:add_le(f.five_3, buffer(48, 4))
arraytree:add_le(f.five_4, buffer(52, 4))
-- This is below 'five' inside dissector function
subtree:add_le(f.pointer, buffer(56, 4))
--[[ This comments out the str array code
-- Array handling for str
local arraytree = subtree:add_le("str: string array", buffer(60, 24))
local subarraytree = arraytree:add_le("str[0]: string array", buffer(60, 8))
subarraytree:add_le(f.str_0_0, buffer(60, 2))
subarraytree:add_le(f.str_0_1, buffer(62, 2))
subarraytree:add_le(f.str_0_2, buffer(64, 2))
subarraytree:add_le(f.str_0_3, buffer(66, 2))
local subarraytree = arraytree:add_le("str[1]: string array", buffer(68, 8))
subarraytree:add_le(f.str_1_0, buffer(68, 2))
subarraytree:add_le(f.str_1_1, buffer(70, 2))
subarraytree:add_le(f.str_1_2, buffer(72, 2))
subarraytree:add_le(f.str_1_3, buffer(74, 2))
local subarraytree = arraytree:add_le("str[2]: string array", buffer(76, 8))
subarraytree:add_le(f.str_2_0, buffer(76, 2))
subarraytree:add_le(f.str_2_1, buffer(78, 2))
subarraytree:add_le(f.str_2_2, buffer(80, 2))
subarraytree:add_le(f.str_2_3, buffer(82, 2))
]]--
-- This is the last line of the dissector function
end
delegator_register_proto(proto_custom_lua, "Win32", "custom_lua", 74)
''')

