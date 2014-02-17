% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
%
% Zorg options dialog.
%
% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
% Some global vars.
%
/zorg.default 0 def

/zorg.options [
  ""
  "xorg=safe nomodeset"
  "xorg=probe"
  "xorg=off"
] def


% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
% Build zorg list.
%
% ( ) ==> ( )
%
/zorg.init {
  /xmenu.zorg .xm_size array def

  /xmenu xmenu.zorg def

  xmenu .xm_current zorg.default put
  xmenu .xm_list [
    /txt_zorg_default
    /txt_zorg_safe
    /txt_zorg_probe
    /txt_zorg_off
  ] put
  xmenu .xm_title /txt_zorg put

} def


% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
% Update zorg mode.
%
% ( ) ==> ( )
%
/zorg.update {
  /xmenu xmenu.zorg def

  /window.action actRedrawPanel def
} def


% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
% Show zorg menu.
%
% ( ) => ( )
%
/panel.zorg {
  "main" help.setcontext

  window.xmenu
  dup .xmenu xmenu.zorg put
  dup .xmenu.update /zorg.update put
  dup window.init
      window.show
} def


% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
% Return width of panel entry.
%
% ( ) => ( width )
%
/panel.zorg.width {
  /xmenu xmenu.zorg def

  pmenu.width
} def


% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
% Redraw panel entry.
%
% ( panel ) => ( )
%
/panel.zorg.update {
  /xmenu xmenu.zorg def

  pmenu.panel.update
} def


