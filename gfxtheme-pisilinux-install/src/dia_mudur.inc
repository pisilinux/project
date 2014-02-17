% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
%
% Mudur options dialog.
%
% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
% Some global vars.
%
/mudur.default 0 def

/mudur.options [
  ""
  "mudur=safe"
  "mudur=forcefsck"
] def


% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
% Build mudur list.
%
% ( ) ==> ( )
%
/mudur.init {
  /xmenu.mudur .xm_size array def

  /xmenu xmenu.mudur def

  xmenu .xm_current mudur.default put
  xmenu .xm_list [
    % steal some translations from zorg
    /txt_zorg_default
    /txt_zorg_safe
    /txt_mudur_forcefsck
  ] put
  xmenu .xm_title /txt_mudur put

} def


% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
% Update mudur mode.
%
% ( ) ==> ( )
%
/mudur.update {
  /xmenu xmenu.mudur def

  /window.action actRedrawPanel def
} def


% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
% Show mudur menu.
%
% ( ) => ( )
%
/panel.mudur {
  "main" help.setcontext

  window.xmenu
  dup .xmenu xmenu.mudur put
  dup .xmenu.update /mudur.update put
  dup window.init
      window.show
} def


% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
% Return width of panel entry.
%
% ( ) => ( width )
%
/panel.mudur.width {
  /xmenu xmenu.mudur def

  pmenu.width
} def


% - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
% Redraw panel entry.
%
% ( panel ) => ( )
%
/panel.mudur.update {
  /xmenu xmenu.mudur def

  pmenu.panel.update
} def


