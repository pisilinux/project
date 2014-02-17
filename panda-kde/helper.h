#include <kauth.h>

using namespace KAuth;

class Helper : public QObject
{
    Q_OBJECT

    public slots:
        ActionReply save(const QVariantMap &args);



};
