#include <QRadioButton>
#include <QButtonGroup>
#include <QLabel>
#include <QProcess>
#include <QTimer>

//Added by qt3to4:
#include <QVBoxLayout>
#include <QFormLayout>
#include <QBoxLayout>
#include <QGroupBox>

#include "helper.h"

#include <kcmodule.h>
#include <kaboutdata.h>
#include <kapplication.h>
#include <kdialog.h>
#include <klocale.h>
#include <kdebug.h>
#include <kmessagebox.h>
#include <kprocess.h>
#include <kworkspace/kworkspace.h>


// X11 includes
#include <X11/Xlib.h>
#include <X11/Xutil.h>

// OpenGL includes
#include <GL/gl.h>
#include <GL/glext.h>
#include <GL/glx.h>


#include <QX11Info>
#include <kpluginfactory.h>
#include <kpluginloader.h>

#include "panda.h"
#include "panda_parser.h"
#include "panda.moc"

K_PLUGIN_FACTORY(PandaConfigFactory, registerPlugin<PandaConfig>();)
K_EXPORT_PLUGIN(PandaConfigFactory("panda-kde"))


PandaConfig::PandaConfig(QWidget *parent, const QVariantList &args):
    KCModule(PandaConfigFactory::componentData(), parent, args)
{

  // The Main Layout, on top of this are two groupboxes, topBox and bottomBox
  QBoxLayout *layout = new QVBoxLayout(this);
  layout->setMargin(0);

  // Current Driver Information
  QGroupBox *topBox = new QGroupBox(i18n("Current Driver Information"), this );

  QGridLayout *infoLayout = new QGridLayout(this);
  infoLayout->setAlignment(Qt::AlignTop|Qt::AlignLeft);

  topBox->setLayout(infoLayout);
  layout->addWidget(topBox);

  QLabel *iconLabel = new QLabel();
  iconLabel->setAlignment(Qt::AlignCenter);
  iconLabel->setSizePolicy(QSizePolicy::Maximum, QSizePolicy::Maximum);
  iconLabel->setPixmap(KIcon("hwinfo").pixmap(64));

  // Get opengl informations
  pandaParser = new PandaParser();
  pandaParser->getGlStrings();

  // A simple way to set labels to bold
  QFont bFont;
  bFont.setBold(true);

  // Display driver informations
  QLabel *vendorLabel = new QLabel();
  vendorLabel->setFont(bFont);
  vendorLabel->setText(i18n("Vendor:"));

  QLabel *vendorNameLabel = new QLabel();
  vendorNameLabel->setText(pandaParser->glVendor);
  vendorNameLabel->setIndent(10);

  QLabel *rendererLabel = new QLabel();
  rendererLabel->setFont(bFont);
  rendererLabel->setText(i18n("Renderer:"));

  QLabel *rendererNameLabel = new QLabel();
  rendererNameLabel->setText(pandaParser->glRenderer);
  rendererNameLabel->setIndent(10);

  QLabel *versionLabel = new QLabel();
  versionLabel->setFont(bFont);
  versionLabel->setText(i18n("Version:"));
  QLabel *versionNameLabel = new QLabel();
  versionNameLabel->setText(pandaParser->glVersion);
  versionNameLabel->setIndent(10);

  infoLayout->addWidget(iconLabel,1,1,3,1,Qt::AlignCenter);

  infoLayout->addWidget(vendorLabel,1,2,1,1);
  infoLayout->addWidget(vendorNameLabel,1,3,1,1);

  infoLayout->addWidget(rendererLabel,2,2,1,1);
  infoLayout->addWidget(rendererNameLabel,2,3,1,1);

  infoLayout->addWidget(versionLabel,3,2,1,1);
  infoLayout->addWidget(versionNameLabel,3,3,1,1);

  // Driver Settings
  QGroupBox *bottomGroupBox = new QGroupBox(i18n("Driver Preference"), this );
  QVBoxLayout *layout_settings = new QVBoxLayout();
  bottomGroupBox->setLayout(layout_settings);
  layout->addWidget(bottomGroupBox);
  layout->addStretch();

  osDriver = new QRadioButton(i18n("Use the driver developed by the open source community"), bottomGroupBox);
  vendorDriver = new QRadioButton(i18n("Use the proprietary driver provided by the manufacturer"), bottomGroupBox);
  genericDriver = new QRadioButton(i18n("Use the safe driver that provides limited features"), bottomGroupBox);

  QButtonGroup *buttonGroup = new QButtonGroup(bottomGroupBox);
  connect(buttonGroup, SIGNAL(buttonClicked(int)), this, SLOT(changed()));

  buttonGroup->setExclusive(true);
  buttonGroup->addButton(osDriver);
  buttonGroup->addButton(vendorDriver);
  buttonGroup->addButton(genericDriver);

  layout_settings->addWidget(osDriver);
  layout_settings->addWidget(vendorDriver);
  layout_settings->addWidget(genericDriver);

  KAboutData *about = new KAboutData("kcmpanda",
                                      "panda-kde",
                                      ki18n("Video Driver Administration"),
                                      0,
                                      KLocalizedString(),
                                      KAboutData::License_GPL,
                                      ki18n("(c) 2011 Fatih Arslan"),
                                      KLocalizedString(),
                                      "http://www.pardus.org.tr");
  KLocalizedString authorPageText;

  if (about->bugAddress().isEmpty() || about->bugAddress() == "submit@bugs.kde.org")
    authorPageText = ki18n("Please use <a href=\"http://bugs.pardus.org.tr\">http://bugs.pardus.org.tr</a> to report bugs.\n");
  about->setCustomAuthorText(KLocalizedString(), authorPageText);
  about->addAuthor(ki18n("Fatih Arslan"), ki18n("Original author"), "farslan@pardus.org.tr");
  about->setTranslator(ki18nc("NAME OF TRANSLATORS", "Your names"),
                       ki18nc("EMAIL OF TRANSLATORS", "Your emails"));
  setAboutData(about);

  // Needed by Kauth, should be executed after KAboutData
  setNeedsAuthorization(true);
}

PandaConfig::~PandaConfig()
{
    delete pandaParser;
}

void PandaConfig::load()
{

  QString program = "/usr/libexec/panda-helper";

  // Gather which checkboxes do should be enabled or not
  QStringList typeArgs;
  typeArgs << "types";

  QProcess *typeP = new QProcess(this);
  typeP->start(program, typeArgs);
  typeP->waitForFinished();

  QByteArray typeOut = typeP->readAllStandardOutput();
  QStringList driverTypes = QString(typeOut).trimmed().split(",");

  // Which driver is used currently
  QStringList curArgs;
  curArgs << "cur";
  QProcess *curP = new QProcess(this);
  curP->start(program, curArgs);
  curP->waitForFinished();

  QByteArray curOut = curP->readAllStandardOutput();
  QString currentDriver = QString(curOut).trimmed();

  // Set checkboxes
  QString vendor = "vendor";
  QString os = "os";
  QString generic = "generic";

  bool isVendor = (vendor == currentDriver);
  bool isOs = (os == currentDriver);
  bool isGeneric = (generic == currentDriver);

  if (driverTypes.contains(vendor)) {
      if (isVendor)
          vendorDriver->setChecked(true);
  } else {
      vendorDriver->setDisabled(true);
  }

  if (driverTypes.contains(os)) {
      if (isOs)
          osDriver->setChecked(true);
  } else {
      osDriver->setDisabled(true);
  }

  if (driverTypes.contains(generic)) {
      if (isGeneric)
          genericDriver->setChecked(true);
  } else {
      genericDriver->setDisabled(true);
  }

  emit changed(false);
}

void PandaConfig::save()
{
  if (!installMissing()) {
      KMessageBox::error(this, i18n("Unable to apply settings due to missing packages"));
      QTimer::singleShot(0, this, SLOT(changed()));
      return;
  }

  QVariantMap helperargs;

  helperargs["osdriver"] = osDriver->isChecked();
  helperargs["vendordriver"] = vendorDriver->isChecked();
  helperargs["genericdriver"] = genericDriver->isChecked();

  Action *action = authAction();
  action->setArguments(helperargs);

  ActionReply reply = action->execute();

  if (reply.failed()) {
    if (reply.type() == ActionReply::KAuthError) {
        KMessageBox::error(this, i18n("Unable to authenticate/execute the action: %1, %2", reply.errorCode(), reply.errorDescription()));
    } else {
        KMessageBox::error(this, i18n("An internal error occurred"));
    }

    QTimer::singleShot(0, this, SLOT(changed()));
  } else {

      //KMessageBox::information(this, i18n("You have to restart your system "));
    int ret = KMessageBox::questionYesNo(this,
                                i18n("You have to restart your system for the changes to take affect.\n"
                                     "Do you want to restart now?"));
    if(ret == KMessageBox::Yes){

        KWorkSpace::requestShutDown( KWorkSpace::ShutdownConfirmNo,
                                     KWorkSpace::ShutdownTypeReboot,
                                     KWorkSpace::ShutdownModeInteractive);
        qDebug() << "YES";
    }

  }

}

void PandaConfig::defaults()
{
  QString program = "/usr/libexec/panda-helper";

  // Gather which checkboxes do should be enabled or not
  QStringList typeArgs;
  typeArgs << "types";

  QProcess *typeP = new QProcess(this);
  typeP->start(program, typeArgs);
  typeP->waitForFinished();

  QByteArray typeOut = typeP->readAllStandardOutput();
  QStringList driverTypes = QString(typeOut).trimmed().split(",");

  QString vendor = "vendor";
  QString os = "os";
  QString generic = "generic";

  if (!driverTypes.contains(vendor))
      vendorDriver->setDisabled(true);

  if (!driverTypes.contains(os))
      osDriver->setDisabled(true);

  if (!driverTypes.contains(generic))
      genericDriver->setDisabled(true);

  osDriver->setChecked(true);
  emit changed(true);
}

bool PandaConfig::installMissing()
{
  if (!vendorDriver->isChecked())
      return true;

  KProcess p;
  p << "/usr/libexec/panda-helper" << "check";
  p.setOutputChannelMode(KProcess::SeparateChannels);
  if (p.execute())
      return false;

  QString cliOut = QString(p.readAllStandardOutput()).trimmed();
  if (cliOut.isEmpty())
      return true;

  QStringList missingPackages = cliOut.split(",");

  KProcess pmInstall;
  pmInstall << "/usr/bin/pm-install" << "--hide-summary" <<missingPackages;
  pmInstall.setOutputChannelMode(KProcess::SeparateChannels);

  kapp->setOverrideCursor(QCursor(Qt::WaitCursor));
  int failed = pmInstall.execute();

  kapp->restoreOverrideCursor();

  return bool(!failed);
}
