% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
%
% Kernel options dialog.
%
% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
% Some global vars.
%
/kerneloptsinstall.default 0 def

/kerneloptsinstall.options [
  "splash quiet"
  ""
  "apm=off acpi=off mce=off barrier=off ide=nodma idewait=50 i8042.nomux psmouse.proto=bare irqpoll pci=nommconf edd=off"
  "acpi=off"
  "nolapic"
  "bootmem_debug debug debugpat dynamic_printk earlyprintk=vga initcall_debug loglevel=7 mminit_loglevel=4 pnp.debug sched_debug apic=debug"
] def


% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
% Build kerneloptsinstall list.
%
% ( ) ==> ( )
%
/kerneloptsinstall.init {
  /xmenu.kerneloptsinstall .xm_size array def

  /xmenu xmenu.kerneloptsinstall def

  xmenu .xm_current kerneloptsinstall.default put
  xmenu .xm_list [
    /txt_kernel_default
    /txt_zorg_off
    /txt_kernel_safe
    /txt_kernel_noacpi
    /txt_kernel_nolapic
    /txt_kernel_debug
  ] put
  xmenu .xm_title /txt_kernel put

} def


% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
% Update kerneloptsinstall mode.
%
% ( ) ==> ( )
%
/kerneloptsinstall.update {
  /xmenu xmenu.kerneloptsinstall def

  /window.action actRedrawPanel def
} def


% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
% Show kerneloptsinstall menu.
%
% ( ) => ( )
%
/panel.kerneloptsinstall {
  "main" help.setcontext

  window.xmenu
  dup .xmenu xmenu.kerneloptsinstall put
  dup .xmenu.update /kerneloptsinstall.update put
  dup window.init
      window.show
} def


% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
% Return width of panel entry.
%
% ( ) => ( width )
%
/panel.kerneloptsinstall.width {
  /xmenu xmenu.kerneloptsinstall def

  pmenu.width
} def


% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
% Redraw panel entry.
%
% ( panel ) => ( )
%
/panel.kerneloptsinstall.update {
  /xmenu xmenu.kerneloptsinstall def

  pmenu.panel.update
} def


