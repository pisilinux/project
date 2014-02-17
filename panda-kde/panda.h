#ifndef __bell_h__
#define __bell_h__

#include "kcmodule.h"

class QRadioButton;
class PandaParser;

class PandaConfig : public KCModule
{
  Q_OBJECT

 public:
  PandaConfig(QWidget *parent, const QVariantList &args);
  virtual ~PandaConfig();

  void load();
  void save();
  void defaults();
  bool installMissing();

 private:
  QRadioButton    *osDriver;
  QRadioButton    *vendorDriver;
  QRadioButton    *genericDriver;
  PandaParser*     pandaParser;
};

#endif
